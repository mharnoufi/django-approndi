import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_project.settings")
django.setup()

from jobs.models import JobRecord
from django.db.models import Avg, Count, F, Q

top_5_jobs = (
    JobRecord.objects
    .order_by('salary_in_usd')
    .values('job_title','salary_in_usd')
    .distinct()[:5]
)
    # 1. Liste des 5 job titles les mieux payés en USD.
top_5_jobs = (
    JobRecord.objects
    .order_by('salary_in_usd')
    .values('job_title','salary_in_usd')
    .distinct()[:5]
)

    # 2. Salaire moyen par niveau d'expérience.

avg_salary_by_exp = (
    JobRecord.objects
    .values('experience_level')
    .annotate(avg_salary=Avg('salary_in_usd'))
    .order_by('experience_level')
)

    # 3. Nombre de jobs par company _location.

jobs_by_location = (
    JobRecord.objects
    .values('company_location')
    .annotate(count=Count('id'))
    .order_by('-count')

)
    # 4. Ratio de jobs 100% remote

total_jobs = JobRecord.objects.count()
remote_jobs = JobRecord.objects.filter(remote_ratio=100).count()
remote_ratio = (remote_jobs / total_jobs) * 100 if total_jobs > 0 else 0

report_lines = []

report_lines.append("Top 5 des jobs les mieux payés (en USD) :")
for job in top_5_jobs:
    report_lines.append(f"- {job['job_title']}: ${job['salary_in_usd']}")

report_lines.append("\nSalaire moyen par niveau d'expérience :")
for exp in avg_salary_by_exp:
    report_lines.append(f"- {exp['experience_level']}: ${exp['avg_salary']:.2f}")

report_lines.append("\nNombre de jobs par localisation de l'entreprise :")
for loc in jobs_by_location:
    report_lines.append(f"- {loc['company_location']}: {loc['count']}")

report_lines.append(f"\nRatio de jobs 100% remote : {remote_ratio:.2f}%")

report_text = "\n".join(report_lines)

print(report_text)

with open("job_report.txt", "w", encoding="utf-8") as f:
    f.write(report_text)







