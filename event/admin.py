from django.contrib import admin
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import RecurringEventChild

class RecurringEventChildAdmin(ModelAdmin):
    model = RecurringEventChild
    list_display = ('date', 'title')
    ordering = ['date']
    menu_label = 'Recurring Events'


modeladmin_register(RecurringEventChildAdmin)