from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('job', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
