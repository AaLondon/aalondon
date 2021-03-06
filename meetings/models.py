from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from datetime import time
import json
import what3words


WHAT_THREE_WORDS_API_KEY = settings.WHAT_THREE_WORDS_API_KEY
# Create your models here.
class MeetingDay(models.Model):
    value = models.CharField(max_length=10,null=False,blank=False)

    def __str__(self):
        return self.value
    
class MeetingIntergroup(models.Model):
    value = models.CharField(max_length=100,null=False,blank=False)

    def __str__(self):
        return self.value

class MeetingSubType(models.Model):
    code = models.CharField(max_length=5,null=False,blank=False)
    value = models.CharField(max_length=100,null=False,blank=False)
    
    def __str__(self):
        return f'{self.code} - {self.value}'


class Meeting(models.Model):
    MEETING_TYPES = [
    ('F2F', 'Face To Face'),
    ('ONL', 'Online'),
    ('HYB', 'Hybrid'),    
    ]
    type = models.CharField(
        max_length=3,
        choices=MEETING_TYPES,
        null=False,
        blank=False,default='F2F'
        
    )
    submission = models.CharField(max_length=10,null=False,blank=False,default='existing')
    address = models.TextField(blank=True,max_length=300)
    code = models.IntegerField(blank=True,null=True,default=-1)
    days = models.ManyToManyField(to=MeetingDay,related_name='meeting_days')
    intergroup = models.ForeignKey(to=MeetingIntergroup,related_name='meeting_intergroup',null=True,blank=True,on_delete=models.CASCADE)
    time = models.TimeField(null=False,blank=False)
    online_link = models.URLField(max_length=1000,null=True,blank=True)
    online_password = models.CharField(max_length=50,null=True,blank=True)
    payment_details = models.TextField(null=True,blank=True)
    what_three_words = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=False,blank=False,default='doesnotexist@aalondon.com')
    hearing = models.BooleanField(null=True,default=False)
    lat = models.FloatField(blank=True,null=True)
    lng = models.FloatField(blank=True,null=True)
    postcode = models.TextField(max_length=10,null=True,blank=True)
    time = models.TimeField()
    duration = models.TextField(blank=True,max_length=20)
    title = models.TextField()
    wheelchair = models.BooleanField(null=True,default=False)
    day_number = models.IntegerField(blank=True,null=True)
    slug = AutoSlugField(populate_from=['title','postcode','time'], max_length=100)
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
    conference_url = models.URLField(max_length=1000,blank=True,null=True)
    types = models.CharField(max_length=200,blank=True,null=True)
    description = models.TextField(null=True,blank=True)
    notes = models.TextField(null=True,blank=True)
    sub_types = models.ManyToManyField(to=MeetingSubType,blank=True)
    published = models.BooleanField(null=False,blank=False,default=False)

    def __str__(self):

        return self.title

    def meeting_days(self):
        return ",".join([str(p) for p in self.days.all()])
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.title} {self.time} {self.type} {self.id}')
        meeting_time = self.time
        #We only want wagtail backend to do a what3words lookup
        if self.published:
            geocoder = what3words.Geocoder(WHAT_THREE_WORDS_API_KEY)
            res = geocoder.convert_to_coordinates(self.what_three_words)
            if 'coordinates' in res:
                self.lat = res['coordinates']['lat']
                self.lng = res['coordinates']['lng']
        
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

