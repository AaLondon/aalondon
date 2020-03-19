from django.db import models
from django.utils.text import slugify

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


