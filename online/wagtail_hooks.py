from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import OnlineMeeting


class OnlineMeetingAdmin(ModelAdmin):
    model = OnlineMeeting
    menu_icon = 'day'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('title', 'day','platform', 'time', 'link','description','additional_comments','published')
    list_filter = ('day','published')
    search_fields = ('title',)

# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(OnlineMeetingAdmin)