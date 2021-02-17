from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import MeetingNeufList, MeetingDetail


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", MeetingNeufList.as_view()),
    path("<int:pk>/", MeetingDetail.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
