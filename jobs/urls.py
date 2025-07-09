from django.urls import path, include
from .views import dashboard_view, job_detail, job_list
from rest_framework.routers import DefaultRouter
from .views import JobRecordViewSet

router = DefaultRouter()
router.register(r'/jobs', JobRecordViewSet, basename='jobrecord')

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('jobs/', job_list, name='job_list'),
    path('job/<int:pk>/', job_detail, name='job_detail'),
    path('', include(router.urls)),  
]
