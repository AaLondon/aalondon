from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from api import urls as api_urls

from search import views as search_views
from meetings.views import MeetingSearchView,MeetingDetailView

from online.views import OnlineMeetingDetailView,redirect_view,OnlineMeetingCreateView,OnlineMeetingThanksView,OnlineMeetingSearchView
from wagtail.contrib.sitemaps.views import sitemap


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('sentry-debug/', trigger_error),
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),
    url(r'^api/', include(api_urls)),
    path('meetingsearch/', MeetingSearchView.as_view(), name='meeting_search'),
    path('onlinemeetingsearch/', OnlineMeetingSearchView.as_view(), name='online_meeting_search'),
    path('meetings/<slug:slug>/', MeetingDetailView.as_view(), name='meeting-detail'),
    path('onlinemeetings/thanks/', OnlineMeetingThanksView.as_view(), name='online-meeting-thanks'),
    path('onlinemeetings/create/', OnlineMeetingCreateView.as_view(), name='online-meeting-create'),
    path('onlinemeetings/<slug:slug>/', OnlineMeetingDetailView.as_view(), name='online-meeting-detail'),
    
    path('online/zoom-meetings/', redirect_view,name='online-zoom-meetings-redirect'),
    url('^sitemap\.xml$', sitemap),
    
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

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
