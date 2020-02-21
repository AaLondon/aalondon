from django.contrib import admin
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import RecurringEventChild,EventType

class RecurringEventChildAdmin(ModelAdmin):
    model = RecurringEventChild
    list_display = ('date', 'title')
    ordering = ['date']
    menu_label = 'Recurring Events'

class EventTypeAdmin(ModelAdmin):
    model = EventType
    list_display = ('value', )
    

modeladmin_register(EventTypeAdmin)

modeladmin_register(RecurringEventChildAdmin)