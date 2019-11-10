from django.shortcuts import render
from django.views.generic import TemplateView

class MeetingSearchView(TemplateView):
    template_name = "meeting_search.html"

