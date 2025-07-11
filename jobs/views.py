from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import JobRecord
from .serializers import JobRecordSerializer
from feedback.models import Feedback
from django.http import JsonResponse

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
    feedbacks = job.feedbacks.all()  # related_name='feedbacks'

    if request.method == 'POST':
        author = request.POST.get('author')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if author and rating and comment:
            feedback = Feedback.objects.create(
                job=job,
                author=author,
                rating=int(rating),
                comment=comment
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Réponse JSON pour requête AJAX
                return JsonResponse({
                    'success': True,
                    'feedback': {
                        'author': feedback.author,
                        'rating': feedback.rating,
                        'comment': feedback.comment,
                    }
                })
            else:
                return redirect('job_detail', pk=job.pk)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Tous les champs sont obligatoires.'})
            else:
                #message d'erreur si besoin
                pass

    return render(request, 'jobs/job_detail.html', {'job': job, 'feedbacks': feedbacks})

def job_list(request):
    selected_title = request.GET.get('job_title')
    if selected_title:
        jobs = JobRecord.objects.filter(job_title=selected_title)
    else:
        jobs = JobRecord.objects.all()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Requête AJAX : retourne un JSON
        data = [{
            'id': job.pk,
            'job_title': job.job_title,
            'company_location': job.company_location,
            'salary_in_usd': job.salary_in_usd,
        } for job in jobs]
        return JsonResponse({'jobs': data})

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
