from django.shortcuts import render
from django.views.generic import TemplateView,DetailView
from .models import OnlineMeeting
from django.utils import timezone
from service.models import ServicePage



class OnlineMeetingDetailView(DetailView):
    model = OnlineMeeting

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context



