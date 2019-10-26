from django.core.management.base import BaseCommand
from pcndodger.suspensions.models import PostCode, Borough, Road, PostCodeToRoad
import pandas as pd
from django.db import connection
import re
import environ

ROOT_DIR = environ.Path(__file__) - 5  
print(ROOT_DIR)
APPS_DIR = ROOT_DIR.path('pcndodger')

# Load operating system environment variables and then prepare to use them
env = environ.Env()

class Command(BaseCommand):
    help = 'import csv of postcode road mapping'

    def handle(self, *args, **options):
        #Import csv
        csv_file = str(ROOT_DIR.path('postcodes.csv'))
        df = pd.read_csv(csv_file)  # doctest: +SKIP
        #Add to django bulk or one by one?
        print(df.head())


        for i, d in df.iterrows():
             
            postcode_compressed = re.sub('\s+', '', d.postcode).strip()
            print(f'{d.postcode} xxx {postcode_compressed}')
            borough, created = Borough.objects.get_or_create(value='Camden')

            print(borough)

            postcode, created = PostCode.objects.get_or_create(value=d.Postcode,value_compressed=postcode_compressed, latitude=d.Latitude,
        #                                                 longitude=d.Longitude, easting=d.Easting,\
        #                                                 northing=d.Northing,borough=borough,ward=d.Ward)
        #         postcode.save()
            

        



