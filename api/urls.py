from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, ApplicationViewSet, RecruiterAnalyticsAPIView

app_name = 'api'

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
    path('recruiter/analytics/', RecruiterAnalyticsAPIView.as_view(), name='recruiter_analytics'),
]
