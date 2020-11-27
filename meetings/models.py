from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from datetime import time
import json

# Create your models here.

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
    slug = AutoSlugField(populate_from=['title','day','postcode','time'], max_length=100)
    day_rank = models.IntegerField(blank=True,null=True)
    group = models.TextField(blank=True,null=True)
    group_id = models.IntegerField(blank=True,null=True)
    intergroup = models.CharField(blank=True,max_length=100,null=True)
    intergroup_id = models.IntegerField(blank=True,null=True)
    detail = models.TextField(blank=True,null=True)
    time_band = models.CharField(blank=True,max_length=10,null=True)
    covid_open_status = models.BooleanField(null=False,default=False)    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    conference_url = models.URLField(blank=True,null=True)
    types = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):

        return self.title
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.title} {self.day} {self.time} ')
        meeting_time = self.time
        
        if meeting_time > time(0, 0) and meeting_time <= time(12,0):
            self.time_band = 'morning'
        elif meeting_time > time(12,0) and meeting_time <= time(18,0):
            self.time_band = 'afternoon'
        else:
            self.time_band = 'evening'
        
        
        super(Meeting, self).save(*args, **kwargs)

    def get_absolute_url(self):  

        return reverse("meeting-detail", kwargs={"pk": self.pk})


    def set_types(self, x):
        self.types = json.dumps(x)

    def get_types(self):
        # JSON only supports double-quoted values
        if self.types:
            return json.loads(self.types.replace("'", "\""))
        else:
            return []

