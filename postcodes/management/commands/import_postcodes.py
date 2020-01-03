import pandas as pd
from django.core.management.base import BaseCommand
from core.dbimport.bulk import BulkCreateManager
import environ
#from django_pandas.io import read_frame
from postcodes.models import Postcode


# Load operating system environment variables and then prepare to use them
env = environ.Env()

class Command(BaseCommand):
    help = 'import csv of postcodes in bulk, meant to only run once in the beginning of the project'

    def handle(self, *args, **options):
        df_postcodes = pd.read_csv('imports/postcodeslnglat.csv')
        Postcode.objects.all().delete()

        
         
        # Import PostCodes 
        bulk_mgr = BulkCreateManager(chunk_size=10000)
        for index,row in df_postcodes.iterrows():
            bulk_mgr.add(Postcode(postcode=row[0],longitude=row[2],latitude=row[1]))
            print(row[0])
        bulk_mgr.done()
        
        


