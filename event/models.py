from django.db import models
from django.utils.text import slugify
from django.db.models import Avg, Case, Count

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
from postcodes.models import Postcode
from service.models import ServicePage
from django.utils import dateformat
import datetime



class EventType(models.Model):
    value = models.CharField(max_length=40)

    def __str__(self):
        return self.value

class SingleDayEvent(Page):
    body = RichTextField()
    post_date = models.DateField("Post Date")
    start_date = models.DateField("Event Date")
    start_time = models.TimeField("Start Time")
    end_time = models.TimeField("End Time")
    address = models.TextField(blank=False,null=False)
    postcode = models.CharField(max_length=10,blank=False,null=False)
    longitude = models.FloatField(blank=True,null=True)
    latitude = models.FloatField(blank=True,null=True)
    type = models.ForeignKey(to=EventType, on_delete=models.SET_NULL,null=True)
    


    content_panels = Page.content_panels + [
    FieldPanel('post_date'),
    FieldPanel('start_date'),
    FieldPanel('body', classname="full"),
    FieldPanel('address'),
    FieldPanel('postcode'),
    FieldPanel('start_time'),
    FieldPanel('end_time'),
    FieldPanel('type'),
    FieldPanel('latitude'),
    FieldPanel('longitude'),

    
    ]
    subpage_types = []

class MultiDayEvent(Page):
    body = RichTextField()
    post_date = models.DateField("Post date")
    start_date = models.DateField("Start Date")
    end_date = models.DateField("End Date")
    address = models.TextField(blank=False,null=False)
    postcode = models.CharField(max_length=10,blank=False,null=False)
    longitude = models.FloatField(blank=True,null=True)
    latitude = models.FloatField(blank=True,null=True)
    type = models.ForeignKey(to=EventType, on_delete=models.SET_NULL,null=True)
   
    content_panels = Page.content_panels + [
    
    FieldPanel('body', classname="full"),
    FieldPanel('address'),
    FieldPanel('postcode'),
    FieldPanel('post_date'),
    FieldPanel('start_date'),
    FieldPanel('end_date'),
    FieldPanel('type'),
    FieldPanel('latitude'),
    FieldPanel('longitude'),
    
    ]
    subpage_types = []


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
    post_date = models.DateField("Post date")
    start_time = models.TimeField("Start Time")
    end_time = models.TimeField("End Time")
    recurring = models.BooleanField(default=False)
    recurring_index = models.IntegerField(choices=RECURRING_INDEX_OPTIONS,null=True,blank=True)
    recurring_day = models.IntegerField(choices=RECURRING_DAY_OPTIONS,null=True,blank=True)
    recurring_month = models.IntegerField(choices=RECURRING_MONTH_OPTIONS,null=True,blank=True)
    recurring_start_date = models.DateField(null=False,blank=False)
    recurring_end_date = models.DateField(null=False,blank=False)
    address = models.TextField(blank=False,null=False)
    postcode = models.CharField(max_length=10,blank=False,null=False)
    longitude = models.FloatField(blank=True,null=True)
    latitude = models.FloatField(blank=True,null=True)
    type = models.ForeignKey(to=EventType, on_delete=models.SET_NULL,null=True)


    
    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('post_date'),
        
        FieldPanel('body', classname="full"),
        FieldPanel('address'),
        FieldPanel('postcode'),
        MultiFieldPanel(
        [
        FieldPanel('recurring_index'),
        FieldPanel('recurring_day'),
        FieldPanel('recurring_month'),
        FieldPanel('recurring_start_date'),
        FieldPanel('recurring_end_date')],
        heading="Recurrance Options",),
        FieldPanel('start_time'),
        FieldPanel('end_time'),
        FieldPanel('type'),
        FieldPanel('latitude'),
        FieldPanel('longitude'),
        
       #InlinePanel('override_dates', label='override dates'),
    ]

    subpage_types = ['event.RecurringEventChild']

   

class RecurringEventChild(Page):
    
    body = RichTextField()
    post_date = models.DateField("Post date")
    start_date = models.DateField("Start date")
    start_time = models.TimeField("Start Time")
    end_time = models.TimeField("End Time")
    address = models.TextField(blank=False,null=False)
    postcode = models.CharField(max_length=10,blank=False,null=False)
    longitude = models.FloatField(blank=True,null=True)
    latitude = models.FloatField(blank=True,null=True)
    type = models.ForeignKey(to=EventType, on_delete=models.SET_NULL,null=True)
    class Meta:
        ordering = ['start_date']

    parent_page_type = [
        'event.RecurringEventParent',  
    ]

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('start_date'),
        FieldPanel('address'),
        FieldPanel('postcode'),
        FieldPanel('start_time'),
        FieldPanel('end_time'),
        FieldPanel('type'),
        FieldPanel('latitude'),
        FieldPanel('longitude'),
        
    ]
    subpage_types = []

class EventIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
    
    def get_context(self, request):
        today = datetime.datetime.today()
        context = super().get_context(request)
        children = MultiDayEvent.objects.none()
         
        event_type = request.GET.get('event_type', None)

        # get event counts
        type_counts_recurring = list(RecurringEventChild.objects.values('type__value').annotate(total=Count('type__value')).order_by())
        type_counts_multi = list(MultiDayEvent.objects.values('type__value').annotate(total=Count('type__value')).order_by()) 
        type_counts_single = list(SingleDayEvent.objects.values('type__value').annotate(total=Count('type__value')).order_by()) 
        event_counts = {}
        all_counts = type_counts_recurring + type_counts_multi + type_counts_single

        for row in all_counts:
            event_counts['All'] = event_counts.get('All',0) + row['total']
            event_counts[row['type__value']] = event_counts.get(row['type__value'],0) +   row['total']

        # Add extra variables and return the updated context
        recurring_parents=RecurringEventParent.objects.child_of(self).live()
        for parent in recurring_parents:
            children = children | RecurringEventChild.objects.child_of(parent).live()    
        
        multis_qs = MultiDayEvent.objects.filter(end_date__gte=today) 
        singles_qs = SingleDayEvent.objects.filter(start_date__gte=today) 
        children_qs = RecurringEventChild.objects.filter(start_date__gte=today)

        if event_type and event_type != 'All':
            multis_qs = multis_qs.filter(type__value__iexact=event_type)
            singles_qs = singles_qs.filter(type__value__iexact=event_type)
            children_qs = children_qs.filter(type__value__iexact=event_type)

            
        multis = list(multis_qs) 
        singles = list(singles_qs) 
        children = list(children_qs)  

        alls = singles + multis + children
        #if event_type:
         #   alls = alls.filter(type=1) 
        sorted_alls = sorted(alls, key=lambda event : event.start_date )   

        context['event_entries'] = sorted_alls
        context['event_counts'] = event_counts
        context['active'] = event_type or 'All'
        
        return context
    
    subpage_types = ['event.RecurringEventParent','event.MultiDayEvent','event.SingleDayEvent']



### FUNCTIONS ####
def daterange(start, end, step=datetime.timedelta(7)):
    current_date = start
    while current_date <= end:
        yield current_date - step,current_date,current_date + step
        current_date += step

def get_recurrant_dates(day_index,month_index,start_date,end_date):
    recurrant_dates = []
    
    for previous,current,following in daterange(start_date,end_date):
        if  (current.month - start_date.month) % (month_index + 1) == 0:
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
def create_or_update_recurring_children(sender, **kwargs):
   
    new_slugs = []
    now = datetime.datetime.now() 
    parent = kwargs['instance']
    day_index = parent.recurring_index  
    month_index = parent.recurring_month
    start_date = parent.recurring_start_date
    end_date = parent.recurring_end_date
    recurrant_dates = get_recurrant_dates(day_index,month_index,start_date,end_date)
    postcode_obj = Postcode.objects.filter(postcode=parent.postcode).first()
    if postcode_obj:
        parent.longitude = postcode_obj.longitude
        parent.latitude = postcode_obj.latitude 
    
    
    for date in recurrant_dates:
        
        slug = slugify(f'{parent.slug}-{date}')
        new_slugs.append(slug)
        date_output  = datetime.datetime.strftime(date, "%B %d, %Y")
        title = f'{parent.title} {date_output}'
        start_time = parent.start_time
        end_time = parent.end_time
        body = parent.body
        post_date = parent.post_date
        event_type = parent.type
       
        #1. Create child if slug does not exist
        child = RecurringEventChild.objects.filter(slug=slug)
        if not(child):
            
            child = RecurringEventChild(start_date=date,post_date=post_date,title=title,slug=slug,body=body,start_time=start_time,end_time=end_time,postcode=parent.postcode\
                ,longitude=parent.longitude,latitude=parent.latitude\
                    ,address=parent.address,type=event_type)
            parent.add_child(instance=child)
        else:
            child[0].title = title
            child[0].save()

    parent.save()             
    #2. Go through all children - if slug does not match any of the provided dates delete it    
    all_children = parent.get_children()
    all_slugs = set([instance.slug for instance in all_children ])
    new_slugs = set(new_slugs)
    slugs_to_remove = RecurringEventChild.objects.filter(slug__in=all_slugs.difference(new_slugs))
    slugs_to_remove.delete()

    


def add_longitude_latitude(sender,**kwargs):
    obj = kwargs['instance']
    postcode_obj = Postcode.objects.filter(postcode=obj.postcode).first()
    if postcode_obj:
        obj.longitude = postcode_obj.longitude
        obj.latitude = postcode_obj.latitude     
    obj.save()

    


    
    

# Register listeners for each page model class
page_published.connect(create_or_update_recurring_children, sender=RecurringEventParent)
page_published.connect(add_longitude_latitude, sender=SingleDayEvent)
page_published.connect(add_longitude_latitude, sender=MultiDayEvent)
