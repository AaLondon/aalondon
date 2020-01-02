import pandas as pd
from django.core.management.base import BaseCommand
from postcodes.models import Postcode
import environ


def read_in_chunks(file_object): 
    """Lazy function (generator) to read a file piece by piece. 
        Default chunk size: 1k.""" 
    while True: 
        data = file_object.readline()
        if not data: 
            break 
        yield data   
# Load operating system environment variables and then prepare to use them
env = environ.Env()

class Command(BaseCommand):
    help = 'import csv of postcodes in bulk, meant to only run once in the beginning of the project'

    def handle(self, *args, **options):
        f = open('imports/postcodes.csv') 
        fw = open("imports/postcodeslnglat.csv", "w")
        
        for piece in read_in_chunks(f):
            print(piece)
            row = piece.split(',')
            fw.write(f'{row[0]},{row[2]},{row[3]}\n') 
        
            

        



