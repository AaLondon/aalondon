from django.db import models
from meetings.models import Meeting
from service.models import ServicePage
from wagtail.core.models import Orderable,Page
from datetime import datetime,timedelta
from django.db.models import Q
from django.core import serializers
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Collection, Page
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailmenus.models import AbstractLinkPage



class LinkPage(AbstractLinkPage):
    pass
    
    


class StandardIndexPage(Page):
    pass

class StandardPage(Page):
    """
    A generic content page. On this demo site we use it for an about page but
    it could be used for any type of page content that only needs a title,
    image, introduction and body field
    """

    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        StreamFieldPanel('body'),
        ImageChooserPanel('image'),
    ]


class Notice(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    link_page = models.ForeignKey(
        Page,
        verbose_name=_('link to an internal page'),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    link = models.URLField("External link", blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('link_page'),
        FieldPanel('link'),
        
    ]

    class Meta:
        abstract = True


class HomePageNotices(Orderable, Notice):
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='notices')

class HomePage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ],null=True)
    
    def get_context(self, request):
        context = super().get_context(request)  

        # Add extra variables and return the updated context
        now = datetime.now() 
        day_name_today = now.strftime("%A")
        tomorrow = now + timedelta(days=1   ) 
        day_name_tomorrow = tomorrow.strftime("%A")
        #meetings = Meeting.objects.filter((Q(day=day_name_now) & Q(time__gte=now.time()))|(Q(day=day_name_tomorrow) & Q(time__lte=now.time())))
        
        meetings_today = Meeting.objects.filter((Q(day=day_name_today) & Q(time__gte=now.time()))).order_by('time')
        meetings_tomorrow = Meeting.objects.filter((Q(day=day_name_tomorrow) & Q(time__lte=now.time()))).order_by('time')
        
        data = serializers.serialize('json', list(meetings_today), fields=('title','time'))
        context['meetings_today'] = data 
        context['meetings_tomorrow'] = meetings_tomorrow 
        context['day_name_tomorrow'] = day_name_tomorrow
        context['day_name_today'] = day_name_today
        
        context['notices'] = context['page'].notices.all()
        
        
        


        return context
    
    content_panels = Page.content_panels + [
    StreamFieldPanel('body'),
    InlinePanel('notices', label="notices"),
        
    ]
    subpage_types = ['event.EventIndexPage','service.ServiceIndexPage','online.OnlineIndexPage','StandardIndexPage','StandardPage','LinkPage']
