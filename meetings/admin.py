from django.contrib import admin

# Register your models here.
from .models import Meeting,MeetingIntergroup
from wagtail.core.models import Page

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(MeetingIntergroup)
class MeetingIntergroupAdmin(admin.ModelAdmin):
    search_fields = ['value']
