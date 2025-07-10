from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import JobRecord
from .serializers import JobRecordSerializer
from feedback.models import Feedback


def dashboard_view(request):
    total_jobs = JobRecord.objects.count()
    average_salary = JobRecord.objects.aggregate(Avg('salary_in_usd'))['salary_in_usd__avg']
    total_countries = JobRecord.objects.values('employee_residence').distinct().count()

    context = {
        'total_jobs': total_jobs,
        'average_salary': round(average_salary, 2) if average_salary else 0,
        'total_countries': total_countries,
    }
    return render(request, 'jobs/dashboard.html', context)

def job_detail(request, pk):
    job = get_object_or_404(JobRecord, pk=pk)
    feedbacks = job.feedbacks.all()  # related_name='feedbacks' dans Feedback model

    if request.method == 'POST':
        author = request.POST.get('author')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if author and rating and comment:
            Feedback.objects.create(
                job=job,
                author=author,
                rating=int(rating),
                comment=comment
            )
            return redirect('job_detail', pk=job.pk)

    return render(request, 'jobs/job_detail.html', {'job': job, 'feedbacks': feedbacks})

def job_list(request):
    selected_title = request.GET.get('job_title')
    if selected_title:
        jobs = JobRecord.objects.filter(job_title=selected_title)
    else:
        jobs = JobRecord.objects.all()

    job_titles = JobRecord.objects.values_list('job_title', flat=True).distinct()

    context = {
        'jobs': jobs,
        'job_titles': job_titles,
        'selected_title': selected_title,
    }
    return render(request, 'jobs/job_list.html', context)

class JobRecordViewSet(viewsets.ModelViewSet):
    queryset = JobRecord.objects.all()
    serializer_class = JobRecordSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly]

    # Nouveaux Filtres:
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['job_title', 'employee_residence'] # Champs de recherche
