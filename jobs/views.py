from django.shortcuts import render
from django.db.models import Avg, Count
from .models import JobRecord

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
    return render(request, 'jobs/job_detail.html', {'job': job})