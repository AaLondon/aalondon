from django.db import models
from meetings.models import Meeting
from wagtail.core.models import Page


class HomePage(Page):
    pass

    def get_context(self, request):
        context = super().get_context(request)

        # Add extra variables and return the updated context
        context['meetings'] = Meeting.objects.all()
        return context
