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
    response = redirect('/onlinemeetingsearch')
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
        form.fields['title'].widget = forms.TextInput(attrs={'placeholder': 'Name of meeting'})
        form.fields['link'].widget = forms.TextInput(attrs={'placeholder': 'Please use a zoom url with password link e.g. https://zoom.us/j/123456789?pwd=ABCDEFGc2FEK2NVZ1c5d3Z0OEJuQT09'})
        form.fields['email'].widget = forms.TextInput(attrs={'placeholder': 'This email is for internal communications only and will not be displayed on the site'})
        form.fields['description'].widget = forms.TextInput(attrs={'placeholder': 'Any other meeting details that you would like to be on the meeting detail page? e.g. attendeed limits,expected etiquette?'})
        form.fields['additional_comments'].widget = forms.TextInput(attrs={'placeholder': 'Do you have any additional comments/concerns you need to communiacate to us? We can get back to you by your email'})


        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Online meeting create'

        return context


class OnlineMeetingThanksView(TemplateView):
    template_name = 'online/onlinemeeting_thanks.html'





class OnlineMeetingSearchView(TemplateView):
    template_name = "online/onlinemeeting_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Online meeting search'

        return context
 
