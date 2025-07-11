from django.db import models
from jobs.models import JobRecord

class Feedback(models.Model):
    job = models.ForeignKey(JobRecord, on_delete=models.CASCADE, related_name='feedbacks')
    author = models.CharField(max_length=100)
    comment = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField()  # 1 à 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job.job_title} - {self.rating}/5"
