from django.db import models

# Create your models here.

class Meeting(models.Model):
    address = models.TextField(max_length=300)
    code = models.IntegerField()
    day = models.TextField(max_length=10)
    hearing = models.BooleanField()
    lat = models.FloatField()
    lng = models.FloatField()
    postcode = models.TextField(max_length=10)
    time = models.TimeField()
    duration = models.TextField(max_length=20)
    title = models.TextField()
    wheelchair = models.BooleanField()
    

    def __str__(self):
        return self.title
    