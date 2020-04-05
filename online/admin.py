from django.contrib import admin

# Register your models here.
from .models import OnlineMeeting

class OnlineMeetingAdmin(admin.ModelAdmin):
    search_fields = ['title']

admin.site.register(OnlineMeeting,OnlineMeetingAdmin)