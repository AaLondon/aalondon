from django.urls import reverse
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from meetings.views import MeetingWagtailUpdateView
from .models import Meeting, EmailContact,MeetingSubType
from django.db.models import Q
from wagtail.core.models import Page
from wagtail.contrib.modeladmin.helpers import (
    AdminURLHelper,
    ButtonHelper,
)
from wagtail.contrib.modeladmin.views import IndexView
from django.utils.decorators import method_decorator
from datetime import timedelta

from django.urls import re_path

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from djqscsv import render_to_csv_response
from wagtail.contrib.modeladmin.helpers import (
    AdminURLHelper,
    ButtonHelper,
)
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import IndexView
from wagtail.search.utils import OR


class ExportButtonHelper(ButtonHelper):
    export_button_classnames = ["icon", "icon-download"]

    def export_button(self, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []

        classnames = self.export_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        text = _("Export {} to CSV".format(self.verbose_name_plural.title()))

        return {
            "url": self.url_helper.get_action_url(
                "export", query_params=self.request.GET
            ),
            "label": text,
            "classname": cn,
            "title": text,
        }


class ExportAdminURLHelper(AdminURLHelper):
    non_object_specific_actions = ("create", "choose_parent", "index", "export")

    def get_action_url(self, action, *args, **kwargs):
        query_params = kwargs.pop("query_params", None)

        url_name = self.get_action_url_name(action)
        if action in self.non_object_specific_actions:
            url = reverse(url_name)
        else:
            url = reverse(url_name, args=args, kwargs=kwargs)

        if query_params:
            url += "?{params}".format(params=query_params.urlencode())

        return url

    def get_action_url_pattern(self, action):
        if action in self.non_object_specific_actions:
            return self._get_action_url_pattern(action)

        return self._get_object_specific_action_url_pattern(action)


class ExportView(IndexView):
    model_admin = None

    def export_csv(self):
        if (self.model_admin is None) or not hasattr(
            self.model_admin, "csv_export_fields"
        ):
            data = self.queryset.all().values()
        else:
            data = (
                self.queryset.all().values(*self.model_admin.csv_export_fields)
            )
        return render_to_csv_response(
            data,
            # field_header_map={
            #     "therapist_name": "Therapist",
            #     "client_name": "Client",
            #     "appointment_date": "Appointment Date",
            # },
            field_order=[
                "title",
            ],
        )

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        return self.export_csv()


class ExportModelAdminMixin(object):
    button_helper_class = ExportButtonHelper
    url_helper_class = ExportAdminURLHelper
    export_view_class = ExportView

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls += (
            re_path(
                self.url_helper.get_action_url_pattern("export"),
                self.export_view,
                name=self.url_helper.get_action_url_name("export"),
            ),
        )
        return urls

    def export_view(self, request):
        kwargs = {"model_admin": self}
        view_class = self.export_view_class
        return view_class.as_view(**kwargs)(request)

class MeetingAdmin(ExportModelAdminMixin, ModelAdmin):
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
        "published",
        "created",
        "updated",
        'updated_by',    

    )
    list_filter = ("days", "published")
    search_fields =  ["title",]
    form_fields_exclude = ['updated_by','lat','lng','duration','slug','day_rank','group','group_id','time_band','code','day_number']
    edit_view_class = MeetingWagtailUpdateView
    index_template_name = "wagtailadmin/meeting_admin.html"
    csv_export_fields = [
           "address",
        "created",
        "days__value",
        "description",
        "duration",
        "email",
        "email_confirmed",
        "time",
        "end_time",
        "gso_opt_out",
        "id",
        "intergroup",
        "lat",
        "lng",
        "location",
        "note_expiry_date",
        "notes",
        "online_link",
        "online_password",
        "postcode",
        "postcode_prefix",
        "published",
        "slug",
        "submission",
        "temporary_changes",
        "time_band",
        "title",
        "tradition_7_details",
        "type",
        "updated",
        "updated_by",
        "updated_by_id",
        "what_three_words",
    
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(Q(email_confirmed="PRE") | Q(email_confirmed="CONFIRMED"))



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
    search_fields = ["first_name", "last_name"]


class MeetingSubTypeAdmin(ModelAdmin):
    model = MeetingSubType
    menu_icon = "organisation"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = (
        False  # or True to exclude pages of this type from Wagtail's explorer view
    )
    


modeladmin_register(MeetingSubTypeAdmin)
modeladmin_register(EmailContactAdmin)

# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(MeetingAdmin)
