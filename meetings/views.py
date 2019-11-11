from django.shortcuts import render
from django.views.generic import TemplateView,DetailView
from .models import Meeting
from django.utils import timezone

class MeetingSearchView(TemplateView):
    template_name = "meetings/meeting_search.html"

class MeetingDetailView(DetailView):
    model = Meeting

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context



