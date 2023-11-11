from django.contrib import admin

# Register your models here.
from .models import Meeting
from wagtail.core.models import Page

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    search_fields = Page.search_fields + ['title']


