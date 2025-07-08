from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_list, name='feedback_list'),
    path('add/', views.feedback_add, name='feedback_add'),
]
