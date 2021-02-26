from django.contrib import admin

# Register your models here.
from .models import Meeting

class MeetingAdmin(admin.ModelAdmin):
    search_fields = ['title']

admin.site.register(Meeting,MeetingAdmin)

