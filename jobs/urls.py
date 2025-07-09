from django.urls import path
from .views import dashboard_view, job_detail
from rest_framework.routers import DefaultRouter
from .views import JobRecordViewSet

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('job/<int:pk>/', job_detail, name='job_detail'), 
]

router = DefaultRouter()
router.register(r'jobs', JobRecordViewSet)

urlpatterns = router.urls
