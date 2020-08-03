from django.db import models
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from datetime import time

# Create your models here.


MEETING_TYPE_CHOICES = [
    (0, 'Physical'),
    (1, 'Online'),
    (2, 'Hybrid'),   
]
class Meeting(models.Model):
    address = models.TextField(blank=True,max_length=300)
    code = models.IntegerField(blank=True,)
    day = models.TextField(max_length=10)
    hearing = models.BooleanField()
    lat = models.FloatField(blank=True,null=True)
    lng = models.FloatField(blank=True,null=True)
    postcode = models.TextField(max_length=10)
    time = models.TimeField()
    duration = models.TextField(blank=True,max_length=20)
    title = models.TextField()
    wheelchair = models.BooleanField()
    day_number = models.IntegerField(blank=True,null=True)
    slug = AutoSlugField(populate_from=['title','day','postcode'], max_length=100)
    day_rank = models.IntegerField(blank=True,null=True)
    intergroup = models.CharField(blank=True,max_length=100,null=True)
    detail = models.TextField(blank=True,null=True)
    time_band = models.CharField(blank=True,max_length=10,null=True)
    covid_open_status = models.BooleanField(null=False,default=False)
    meeting_type = models.IntegerField(choices=MEETING_TYPE_CHOICES,default=0)


    
    

    def __str__(self):

        return self.title
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.title} {self.day}')
        meeting_time = self.time
        
        if meeting_time > time(0, 0) and meeting_time <= time(12,0):
            self.time_band = 'morning'
        elif meeting_time > time(12,0) and meeting_time <= time(18,0):
            self.time_band = 'afternoon'
        else:
            self.time_band = 'evening'
        
        
        super(Meeting, self).save(*args, **kwargs)
