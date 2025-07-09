from rest_framework import serializers
from .models import JobRecord, Contract, Skill, Industry, Candidate ,Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['type_code', 'description']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name']

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['name','email', 'location']

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['name','email', 'location']


class JobRecordSerializer(serializers.ModelSerializer):
    contract   = ContractSerializer(read_only=True)
    skills     = SkillSerializer(many=True, read_only=True)
    industry   = IndustrySerializer(read_only=True)
    candidate  = CandidateSerializer(read_only=True)

    class Meta:
        model  = JobRecord
        fields = [
            "id",
            "work_year", "experience_level",
            "contract",
            "job_title",
            "industry",
            "salary", "salary_currency", "salary_in_usd",
            "employee_residence", "remote_ratio",
            "company_location", "company_size",
            "candidate",
            "skills",
        ]