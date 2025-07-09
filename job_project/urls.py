from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from feedback.views import FeedbackViewSet

router = DefaultRouter()
router.register(r'feedbacks', FeedbackViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("jobs.urls")),
    path("", include("feedback.urls")),
    path("api/", include(router.urls)),

    path('admin/', admin.site.urls),
    path('api/', include('jobs.urls')),
    path('api/', include('feedback.urls')), 
]
