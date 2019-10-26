import pandas as pd
from django.core.management.base import BaseCommand
from core.dbimport.bulk import BulkCreateManager
from pcndodger.suspensions.models import Borough,PostCode,PostCodeToRoad,Road
import environ
from django_pandas.io import read_frame

ROOT_DIR = environ.Path(__file__) - 5  
print(ROOT_DIR)
APPS_DIR = ROOT_DIR.path('pcndodger')

# Load operating system environment variables and then prepare to use them
env = environ.Env()

class Command(BaseCommand):
    help = 'import csv of postcodes in bulk, meant to only run once in the beginning of the project'

    def handle(self, *args, **options):
        df_postcodes = pd.read_csv('imports/postcodes.txt')
        PostCode.truncate()
        Borough.truncate()
        Road.truncate()
        
        #clean data
        df_postcodes['postcode'] = df_postcodes['postcode'].str.strip()
        df_postcodes['street'] = df_postcodes['street'].str.strip()
        df_postcodes['street'] = df_postcodes['street'].str.title()
        df_postcodes['borough'] = df_postcodes['borough'].str.strip()
        df_postcodes['borough'] = df_postcodes['borough'].str.title()
        boroughs =list(df_postcodes['borough'].unique())
        df_boroughs = pd.DataFrame(boroughs,columns=['value'])
        bulk_mgr = BulkCreateManager(chunk_size=20)
        
        # Import Boroughs
        for index,row in df_boroughs.iterrows():
            bulk_mgr.add(Borough(value=row[0]))
        bulk_mgr.done()
        df_boroughs_db=pd.DataFrame(list(Borough.objects.all().values('value','id')))
         
        # Import PostCodes 
        df_postcodes = pd.merge(df_postcodes, df_boroughs_db, how='inner', left_on='borough', right_on='value')
        del df_postcodes['value']
        df_distinct_postcodes=df_postcodes[['postcode','id']].drop_duplicates()
        df_distinct_postcodes.head()
        bulk_mgr = BulkCreateManager(chunk_size=1000)
        for index,row in df_distinct_postcodes.iterrows():
            bulk_mgr.add(PostCode(value=row[0],borough_id=row[1]))
        bulk_mgr.done()
        
        # Import Roads
        df_distinct_roads = df_postcodes[['street','id']].drop_duplicates()
        df_distinct_roads.head()
        bulk_mgr = BulkCreateManager(chunk_size=20)
        for index,row in df_distinct_roads.iterrows():
            bulk_mgr.add(Road(value=row[0],borough_id=row[1],valid=1))
        bulk_mgr.done() 

        qs = PostCode.objects.select_related().values('id','value')
        df_postcodes_db = read_frame(qs)

        # Import PostCodesToRoad
        qs = Road.objects.select_related().values('id','value','borough')
        df_roads_db = read_frame(qs)
        df_postcodes = pd.merge(df_postcodes, df_postcodes_db, how='inner', left_on='postcode', right_on='value')
        df_postcodes = df_postcodes.rename(columns={"id_y": "postcode_id", "id_x": "borough_id"})
        df_postcodes = pd.merge(df_postcodes, df_roads_db, how='inner', left_on=['street','borough'], right_on=['value','borough'])
        df_postcodes = df_postcodes.rename(columns={"id": "road_id"})
        df_postcodes_to_road = df_postcodes[['postcode_id','road_id']]
        bulk_mgr = BulkCreateManager(chunk_size=20)
        for index,row in df_postcodes_to_road.iterrows():
            bulk_mgr.add(PostCodeToRoad(postcode_id=row[0],road_id=row[1]))     
        bulk_mgr.done()
            

        



