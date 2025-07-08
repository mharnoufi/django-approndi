from django.urls import path
from .views import dashboard_view, job_detail

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('job/<int:pk>/', job_detail, name='job_detail'), 
]
