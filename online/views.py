from django.shortcuts import render
from django.views.generic import TemplateView,DetailView,CreateView
from .models import OnlineMeeting
from django.utils import timezone
from service.models import ServicePage
from django import forms


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


class OnlineMeetingCreateView(CreateView):
    model = OnlineMeeting
    fields = ['title', 'day','platform', 'time', 'link','email','description','additional_comments']
    success_url = '/onlinemeetings/thanks'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(OnlineMeetingCreateView, self).get_form(form_class)
        form.fields['time'].widget = forms.TextInput(attrs={'placeholder': '24 hour e.g. 14:00 or 15:30'})
        form.fields['link'].widget = forms.TextInput(attrs={'placeholder': 'Please us a password link'})

        return form


class OnlineMeetingThanksView(TemplateView):
    template_name = 'online/onlinemeeting_thanks.html'

