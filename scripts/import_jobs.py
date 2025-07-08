import os
import sys
from pathlib import Path
import django
import csv
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_project.settings")
django.setup()

from jobs.models import JobRecord, Contract, Skill, Industry, Candidate

CSV_PATH = BASE_DIR / "data" / "salaries.csv"  # ou adapte le chemin

created_count = 0
skipped_count = 0

existing_jobs = set(JobRecord.objects.values_list('job_title', 'work_year', 'employee_residence'))
contracts = {c.type_code: c for c in Contract.objects.all()}
industries = {i.name: i for i in Industry.objects.all()}
candidates = {c.email: c for c in Candidate.objects.all()}

jobs_to_create = []

with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        work_year = int(row["work_year"])
        job_title = row["job_title"]
        employee_residence = row["employee_residence"]
        employment_type = row["employment_type"]
        company_location = row["company_location"]
        
        # doublon
        if (job_title, work_year, employee_residence) in existing_jobs:
            skipped_count += 1
            continue
        
        # get ou create
        contract = contracts.get(employment_type)
        if not contract:
            contract = Contract.objects.create(type_code=employment_type, description=employment_type)
            contracts[employment_type] = contract
        
        industry = industries.get("Unknown")
        if not industry:
            industry = Industry.objects.create(name="Unknown", email="unknown@example.com", location=company_location)
            industries["Unknown"] = industry
        
        candidate_email = f"anonymous_{employee_residence}@example.com"
        candidate = candidates.get(candidate_email)
        if not candidate:
            candidate = Candidate.objects.create(name="Anonymous", email=candidate_email, location=employee_residence)
            candidates[candidate_email] = candidate
        
        job = JobRecord(
            work_year=work_year,
            experience_level=row["experience_level"],
            employment_type=employment_type,
            job_title=job_title,
            salary=int(float(row["salary"])),
            salary_currency=row["salary_currency"],
            salary_in_usd=int(float(row["salary_in_usd"])),
            employee_residence=employee_residence,
            remote_ratio=int(row["remote_ratio"]),
            company_location=company_location,
            company_size=row["company_size"],
            contract=contract,
            industry=industry,
            candidate=candidate
        )
        jobs_to_create.append(job)
        created_count += 1

# regroupe insertion 
with transaction.atomic():
    JobRecord.objects.bulk_create(jobs_to_create, batch_size=1000)

print(f"{created_count} JobRecords créés.")
print(f"{skipped_count} doublons ignorés.")
