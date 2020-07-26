from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'meetings', views.MeetingViewSet)




# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('meetings/',views.MeetingsList.as_view()),
    path('meetingsearch/',views.MeetingSearch.as_view()),
    path('onlinemeetingsearch/',views.OnlineMeetingSearch.as_view()),
    path('', include('rest_framework.urls', namespace='rest_framework'))
]
