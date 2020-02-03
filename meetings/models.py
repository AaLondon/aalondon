from django.db import models
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField

# Create your models here.

class Meeting(models.Model):
    address = models.TextField(max_length=300)
    code = models.IntegerField()
    day = models.TextField(max_length=10)
    hearing = models.BooleanField()
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    postcode = models.TextField(max_length=10)
    time = models.TimeField()
    duration = models.TextField(max_length=20)
    title = models.TextField()
    wheelchair = models.BooleanField()
    day_number = models.IntegerField(null=True)
    slug = AutoSlugField(populate_from=['title','day','postcode'])
    day_rank = models.IntegerField(null=True)
    intergroup = models.CharField(max_length=100,null=True)
    detail = models.TextField(null=True)

    def __str__(self):

        return self.title
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Meeting, self).save(*args, **kwargs)