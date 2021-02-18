from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from datetime import time
import json

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

""" class MeetingNeuf(models.Model):
    MEETING_TYPES = [
    ('F2F', 'Face To Face'),
    ('ONL', 'Online'),
    ('HYB', 'Hybrid'),    
    ]
    type = models.CharField(
        max_length=3,
        choices=MEETING_TYPES,
        null=False,
        blank=False
        
    )
    title = models.CharField(max_length=400,null=False,blank=False)
    submission = models.CharField(max_length=10,null=False,blank=False)
    day = models.ManyToManyField(to=MeetingDay,related_name='meeting_days')
    intergroup = models.ForeignKey(to=MeetingIntergroup,related_name='meeting_intergroup',null=True,blank=True,on_delete=models.CASCADE)
    time = models.TimeField(null=False,blank=False)
    online_link = models.URLField(null=True,blank=True)
    online_password = models.CharField(max_length=50,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    postcode = models.CharField(max_length=10,null=True,blank=True)
    payment_details = models.TextField(null=True,blank=True)
    what_three_words = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=False,blank=False)
    description = models.TextField(null=True,blank=True)
    notes = models.TextField(null=True,blank=True)
    sub_types = models.ManyToManyField(to=MeetingSubType,blank=True)


    def __str__(self):
        return self.title
 """

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
    code = models.IntegerField(blank=True,)
    day = models.TextField(max_length=10)
    days = models.ManyToManyField(to=MeetingDay,related_name='meeting_days')
    intergroup = models.ForeignKey(to=MeetingIntergroup,related_name='meeting_intergroup',null=True,blank=True,on_delete=models.CASCADE)
    time = models.TimeField(null=False,blank=False)
    online_link = models.URLField(max_length=1000,null=True,blank=True)
    online_password = models.CharField(max_length=50,null=True,blank=True)
    payment_details = models.TextField(null=True,blank=True)
    what_three_words = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=False,blank=False,default='doesnotexist@aalondon.com')
    hearing = models.BooleanField()
    lat = models.FloatField(blank=True,null=True)
    lng = models.FloatField(blank=True,null=True)
    postcode = models.TextField(max_length=10)
    time = models.TimeField()
    duration = models.TextField(blank=True,max_length=20)
    title = models.TextField()
    wheelchair = models.BooleanField()
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

    def __str__(self):

        return self.title
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.title} {self.time} {self.days.first()} {self.days.last()}')
     
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

