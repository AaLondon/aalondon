from django.shortcuts import render
from django.views.generic import TemplateView,DetailView
from .models import Meeting
from django.utils import timezone
from service.models import ServicePage

class MeetingSearchView(TemplateView):
    template_name = "meetings/meeting_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicepages'] = ServicePage.objects.all()
        return context

class MeetingDetailView(DetailView):
    model = Meeting

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['servicepages'] = ServicePage.objects.all()
        return context



