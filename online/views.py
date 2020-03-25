from django.shortcuts import render
from django.views.generic import TemplateView,DetailView
from .models import OnlineMeeting
from django.utils import timezone
from service.models import ServicePage

from django.shortcuts import redirect

class OnlineMeetingDetailView(DetailView):
    model = OnlineMeeting

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context





def redirect_view(request):
    response = redirect('/')
    return response