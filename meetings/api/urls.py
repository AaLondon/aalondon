from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import MeetingList, MeetingDetail


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", MeetingList.as_view(),name='meeting-list'),
    path("<int:pk>/", MeetingDetail.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
