from django.db import models
from django.utils.text import slugify

# Create your models here.
from wagtail.core.signals import page_published
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import FieldPanel
from wagtail.search import index
import datetime
from django_extensions.db.fields import AutoSlugField
from datetime import time



class OnlineIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
    def get_context(self, request):
        context = super().get_context(request)
        return context
    
    subpage_types = ['online.OnlinePage',]


class OnlinePage(Page):
    body = RichTextField()
    post_date = models.DateField("Post Date")
    content_panels = Page.content_panels + [
        FieldPanel('post_date'),
    FieldPanel('body', classname="full"),
    
    
    ]
    subpage_types = []




class OnlineMeeting(models.Model):
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'
    ALL = 'All'

    DAY_OF_WEEK_CHOICES = [

        (ALL, ALL),    
        (MONDAY, MONDAY),
        (TUESDAY,TUESDAY),
        (WEDNESDAY,WEDNESDAY),
        (THURSDAY,THURSDAY),
        (FRIDAY,FRIDAY),
        (SATURDAY,SATURDAY),
        (SUNDAY,SUNDAY),
      
    ]   

    ZOOM = 'Zoom'
    SKYPE = 'Skype'

    TYPE_CHOICES = [
        (ZOOM,ZOOM),
        (SKYPE,SKYPE),
    ] 

    title = models.CharField(max_length=100)
    day = models.CharField(
        max_length=9,
        choices=DAY_OF_WEEK_CHOICES
    )
    time = models.TimeField()
    platform = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES
    )
    link = models.CharField(max_length=1000)
    description = models.TextField(null=True,blank=True)
    slug = AutoSlugField(populate_from=['title','day'])
    day_number = models.IntegerField(null=True,blank=True)
    additional_comments = models.TextField(null=True,blank=True)
    published = models.BooleanField(null=False,blank=False,default=False)
    email = models.EmailField(null=True,blank=True)
    hearing = models.BooleanField(null=False,blank=False,default=False)
    time_band = models.CharField(blank=True,max_length=10,null=True)


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        days =['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']
        self.day_number = days.index(self.day)
        meeting_time = self.time
        
        if meeting_time > time(0, 0) and meeting_time <= time(12,0):
            self.time_band = 'morning'
        elif meeting_time > time(12,0) and meeting_time <= time(18,0):
            self.time_band = 'afternoon'
        else:
            self.time_band = 'evening'
        
        super().save(*args, **kwargs)


