from django.shortcuts import render, redirect
from django.db.models import Avg
from .models import Feedback
from .forms import FeedbackForm

def feedback_list(request):
    feedbacks = Feedback.objects.select_related('job').all()
    avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg'] or 0
    return render(request, 'feedback/list_feedback.html', {
        'feedbacks': feedbacks,
        'avg_rating': round(avg_rating, 2)
    })

def feedback_add(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback_list')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/add_feedback.html', {'form': form})
