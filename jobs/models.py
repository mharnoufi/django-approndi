from django.db import models

class Contract(models.Model):
    type_code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type_code} - {self.description}"


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class JobRecord(models.Model):
    # Colonnes issues du CSV
    work_year = models.PositiveIntegerField()
    experience_level = models.CharField(max_length=10)
    employment_type = models.CharField(max_length=10)
    job_title = models.CharField(max_length=200)
    salary = models.PositiveIntegerField()
    salary_currency = models.CharField(max_length=10)
    salary_in_usd = models.PositiveIntegerField()
    employee_residence = models.CharField(max_length=10)
    remote_ratio = models.PositiveIntegerField()
    company_location = models.CharField(max_length=10)
    company_size = models.CharField(max_length=10)

    # Relations
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='jobs')
    skills = models.ManyToManyField(Skill, blank=True, related_name='jobs')
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')

    def __str__(self):
        return f"{self.job_title} ({self.work_year})"
    
#from django.db import models
#from jobs.models import JobRecord

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

