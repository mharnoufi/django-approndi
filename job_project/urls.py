from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from feedback.views import FeedbackViewSet

router = DefaultRouter()
router.register(r'feedbacks', FeedbackViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # APIs
    path('api/', include(router.urls)),           # feedback API
    path('api/', include('jobs.urls')),            # job API
    path('api/', include('feedback.urls')),        # si feedback.urls a aussi des APIs

    # Vues classiques
    path('', include('jobs.urls')),
    path('', include('feedback.urls')),
]
