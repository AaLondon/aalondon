from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from .models import Meeting, MeetingSubType
from django.utils import timezone
from service.models import ServicePage
import datetime
from wagtail.contrib.modeladmin.views import EditView
from wagtail.admin import messages
from django.shortcuts import redirect
from django.http import HttpResponse
import base64
import json


class MeetingSearchView(TemplateView):
    template_name = "meetings/meeting_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["description"] = "Meeting search"

        return context

class XmasView(TemplateView):
    template_name = "meetings/xmas.html"


class MeetingDetailView(DetailView):
    model = Meeting

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class MeetingCreateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        meeting_form_data = {
            "formType":  "",
            "subTypes": []
            
        }
        context["meeting_data"] = meeting_form_data
        return context


class MeetingUpdateView(DetailView):
    model = Meeting

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_time = self.object.time or ""
        end_time = self.object.end_time or ""
        if isinstance(start_time, datetime.time):
            start_time = start_time.strftime("%H:%M")
        if isinstance(end_time, datetime.time):
            end_time = end_time.strftime("%H:%M")

        meeting_form_data = {
            "slug": self.object.slug or "",
            "formType": self.object.type or "",
            "title": self.object.title or "",
            "days": [day.value for day in self.object.days.all()] or "",
            "submission": "existing",
            "intergroup": self.object.intergroup or "",
            "startTime": start_time,
            "endTime": end_time,
            "link": self.object.online_link or "",
            "password": self.object.online_password or "",
            "tradition7Details": self.object.tradition_7_details or "",
            "location": self.object.location or "",
            "address": self.object.address or "",
            "postcode": self.object.postcode or "",
            "whatThreeWords": self.object.what_three_words or "",
            "email": "",
            "description": self.object.description or "",
            "notes": "",
            "subTypes": [sub_type.value for sub_type in self.object.sub_types.all()]
            or "",
            "temporary_changes": self.object.temporary_changes or "",
            "note_expiry_date": self.object.note_expiry_date or "",
            "gsoOptOut": False,
        }

        context["meeting_data"] = meeting_form_data
        return context



class MeetingWagtailUpdateView(EditView):
    def form_valid(self, form):
        open = form.cleaned_data['sub_types'].filter(value='Open')
        if not open:
            form.cleaned_data['sub_types']=form.cleaned_data['sub_types'] | MeetingSubType.objects.filter(value='Closed')
        instance = form.save(commit=False)
        instance.updated_by = self.request.user
        
        instance.save()
        
        form.save_m2m()
        messages.success(
            self.request, self.get_success_message(instance),
            buttons=self.get_success_message_buttons(instance)
        )
        return redirect(self.get_success_url())



class EmailConfirmationView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = self.kwargs["token"]
        # token contains meeting data.
        data = json.loads(base64.urlsafe_b64decode(token+"==").decode())
        if Meeting.objects.filter(**data).exists():
            Meeting.objects.filter(**data).update(email_confirmed="CONFIRMED")
        return context
