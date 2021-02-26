from django.shortcuts import render
from django.views.generic import TemplateView,DetailView,CreateView
from meetings.models import Meeting
from django.utils import timezone
from service.models import ServicePage
from django import forms


from django.shortcuts import redirect

class OnlineMeetingDetailView(DetailView):
    model = Meeting
    template_name = 'online/onlinemeeting_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context





def redirect_view(request):
    response = redirect('/onlinemeetingsearch')
    return response




class OnlineMeetingThanksView(TemplateView):
    template_name = 'online/onlinemeeting_thanks.html'





class OnlineMeetingSearchView(TemplateView):
    template_name = "online/onlinemeeting_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Online meeting search'

        return context
 
