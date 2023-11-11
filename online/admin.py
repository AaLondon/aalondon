from django.contrib import admin

# Register your models here.
from .models import OnlineMeeting
from wagtail.core.models import Page

@admin.register(OnlineMeeting)
class OnlineMeetingAdmin(admin.ModelAdmin):
    search_fields = Page.search_fields +['title']

