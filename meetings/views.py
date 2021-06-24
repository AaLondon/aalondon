from django.shortcuts import render
from django.views.generic import TemplateView,DetailView,UpdateView
from django.views.generic.detail import SingleObjectMixin
from .models import Meeting
from django.utils import timezone
from service.models import ServicePage


class MeetingSearchView(TemplateView):
    template_name = "meetings/meeting_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Meeting search'

        return context

class MeetingDetailView(DetailView):
    model = Meeting

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
class MeetingCreateView(TemplateView):


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class MeetingUpdateView(DetailView):
    model = Meeting

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """ formType: '',
        title: '',
        days: '',
        submission: '',
        intergroup: '',
        startTime: '',
        endTime: '',
        link: '',
        password: '',
        paymentLink: '',
        address: '',
        postcode: '',
        whatThreeWords: '',
        email: '',
        description: '',
        notes: '',
        closed: false,
        wheelchair: false,
        signed: false,
        lgbt: false,
        chits: false,
        childFriendly: false,
        outdoors: false,
        creche: false,
        temporaryClosure: false,
        gsoOptIn: false
 """
        context['meeting_data'] = {'formType':'F2F','b':2}
        return context

