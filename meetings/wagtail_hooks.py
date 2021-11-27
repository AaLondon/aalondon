from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Meeting, EmailContact


class MeetingAdmin(ModelAdmin):
    model = Meeting
    menu_icon = "days"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = (
        False  # or True to exclude pages of this type from Wagtail's explorer view
    )
    list_display = (
        "title",
        "meeting_days",
        "submission",
        "time",
        "covid_open_status",
        "published",
        "xmas_open",
    )
    list_filter = ("days", "published")
    search_fields = ("title",)


class EmailContactAdmin(ModelAdmin):
    model = EmailContact
    menu_icon = "organisation"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = (
        False  # or True to exclude pages of this type from Wagtail's explorer view
    )
    list_display = (
        "first_name",
        "last_name",
        "organisation",
        "email",
        "update_to_gso",
    )
    list_filter = ("organisation", "update_to_gso")
    search_fields = ("first_name", "last_name")


modeladmin_register(EmailContactAdmin)

# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(MeetingAdmin)
