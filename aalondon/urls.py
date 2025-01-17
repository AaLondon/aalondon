from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.urls import path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from api import urls as api_urls
from meetings.views import EmailConfirmationView, XmasView

from search import views as search_views
from meetings.views import MeetingSearchView,MeetingDetailView,MeetingUpdateView,MeetingCreateView

from online.views import OnlineMeetingDetailView,redirect_view,OnlineMeetingThanksView,OnlineMeetingSearchView
from wagtail.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView



def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('sentry-debug/', trigger_error),
    re_path(r'^django-admin/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('search/', search_views.search, name='search'),
    path('api/meetingadd/', include('meetings.api.urls')), 
    path('api/', include(api_urls)),
    path("meetings/email-confirmation/<slug:token>/", EmailConfirmationView.as_view(template_name='meetings/meeting_email_confirmed.html'), name="email-confirmation"),
    path('meetingsearch/', MeetingSearchView.as_view(), name='meeting_search'),
    path('xmas/', XmasView.as_view(), name='xmas'),
    
    path('onlinemeetingsearch/', OnlineMeetingSearchView.as_view(), name='online_meeting_search'),
    path('meetings/<slug:slug>/', MeetingDetailView.as_view(), name='meeting-detail'),
    path('onlinemeetings/thanks/', OnlineMeetingThanksView.as_view(), name='online-meeting-thanks'),
    path('onlinemeetings/<slug:slug>/', OnlineMeetingDetailView.as_view(), name='online-meeting-detail'),
    
    path('online/zoom-meetings/', redirect_view,name='online-zoom-meetings-redirect'),
    re_path('^sitemap\.xml$', sitemap),
    path('update/', MeetingCreateView.as_view(template_name='meetings/meeting_form.html'), name='meeting_form'),
    path('update/<slug:slug>/', MeetingUpdateView.as_view(template_name='meetings/meeting_form.html'), name='meeting_form'),
    path('chatbot/', TemplateView.as_view(template_name='chatbot/chatbot.html'), name='chatbot'),

    
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path('', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
