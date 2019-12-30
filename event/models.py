from django.db import models


# Create your models here.
from wagtail.core.signals import page_published



from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
import datetime

class RecurringEventParent(Page):

    RECURRING_INDEX_OPTIONS = [
        (-1,'Last'),
        (0,'First'),
        (1,'Second'),
        (2,'Third'),
        (3,'Fourth'),

    ]

    RECURRING_MONTH_OPTIONS = [
        (0,'Every Month'),
        (1,'Every Second Month'),
        (2,'Every Third Month'),
        
    ]

    RECURRING_DAY_OPTIONS = [
        
        (0,'Monday'),
        (1,'Tuesday'),
        (2,'Wednesday'),
        (3,'Thursday'),
        (4,'Friday'),
        (5,'Saturday'),      
        (6,'Sunday'),
    ]
    # Database fields

    body = RichTextField()
    date = models.DateField("Post date")
    recurring = models.BooleanField(default=False)
    recurring_index = models.IntegerField(choices=RECURRING_INDEX_OPTIONS,null=True,blank=True)
    recurring_day = models.IntegerField(choices=RECURRING_DAY_OPTIONS,null=True,blank=True)
    recurring_month = models.IntegerField(choices=RECURRING_MONTH_OPTIONS,null=True,blank=True)
    recurring_start_date = models.DateField(null=True,blank=True)
    recurring_end_date = models.DateField(null=True,blank=True)



    
    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body', classname="full"),
        MultiFieldPanel(
        [FieldPanel('recurring'),
        FieldPanel('recurring_index'),
        FieldPanel('recurring_day'),
        FieldPanel('recurring_month'),
        FieldPanel('recurring_start_date')],
        heading="Recurrance Options",),
       #InlinePanel('override_dates', label='override dates'),
    ]

    subpage_types = ['RecurringEventChild',]

   

class RecurringEventChild(Page):
    
    child_date = models.DateField(blank=True,null=True) 

    parent_page_type = [
        'events.RecurringEventChild'  
    ]

    content_panels = Page.content_panels + [
        FieldPanel('child_date'),
    ]

class EventIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
    def get_context(self, request):
        context = super().get_context(request)

        # Add extra variables and return the updated context
        events=RecurringEventChild.objects.child_of(self).live()
        events2=RecurringEventChild.objects.child_of(self).live()
        
        
        context['event_entries'] = events.union(events2)
        return context

def daterange(start, end, step=datetime.timedelta(7)):
    current_date = start
    while current_date <= end:
        yield current_date - step,current_date,current_date + step
        current_date += step

def get_recurrant_dates(day_index,day,month_index,start_date,end_date):
    recurrant_dates = []

    for previous,current,following in daterange(start_date,end_date): 
        if day_index == 0 and current.month != previous.month and current.month == following.month:
            recurrant_dates.append(current)
        if day_index == 1 and current.day > 7 and current.day <=14:
            recurrant_dates.append(current)
        if day_index == 2 and current.day > 14 and current.day <=21:
            recurrant_dates.append(current)
        if day_index == 3 and current.day > 21 and current.day <=28:
            recurrant_dates.append(current)     
        if day_index == -1 and current.month != following.month:
            recurrant_dates.append(current)         

    return recurrant_dates 
    


# Do something clever for each model type
def receiver(sender, **kwargs):
    # Do something with blog posts
    parent = kwargs['instance']
    index = parent.recurring_index  
    day_index = parent.recurring_day
    month_index = parent.recurring_month
    start_date = parent.recurring_start_date
    end_date = parent.recurring_end_date
    recurrant_dates = get_recurrant_dates(index,day,month_index,start_date,end_date)
    # event.save()
    #recurring_event = RecurringEventChild(child_date='2019-12-28',title='City Intergroup Feb',slug='city-intergroup-feb')  
    print('x')
    #event.add_child(instance = recurring_event)
    #event.save()
   
    

# Register listeners for each page model class
page_published.connect(receiver, sender=RecurringEventParent)