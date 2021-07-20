from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from .models import Meeting
from django.utils import timezone
from service.models import ServicePage
import datetime


class MeetingSearchView(TemplateView):
    template_name = "meetings/meeting_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["description"] = "Meeting search"

        return context


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
            "formType": self.object.type or "",
            "title": self.object.title or "",
            "days": [day.value for day in self.object.days.all()] or "",
            "submission": "existing",
            "intergroup": self.object.intergroup or "",
            "startTime": start_time,
            "endTime": end_time,
            "link": self.object.online_link or "",
            "password": self.object.online_password or "",
            "paymentLink": self.object.payment_details or "",
            "address": self.object.address or "",
            "postcode": self.object.postcode or "",
            "whatThreeWords": self.object.what_three_words or "",
            "email": "",
            "description": self.object.description or "",
            "notes": "",
            "subTypes": [sub_type.value for sub_type in self.object.sub_types.all()]
            or "",
            "gsoOptIn": False,
        }

        context["meeting_data"] = meeting_form_data
        return context
