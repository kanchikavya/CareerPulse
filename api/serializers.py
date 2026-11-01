from rest_framework import serializers
from accounts.models import User, Company, CandidateProfile
from jobs.models import Job, Application, SavedJob


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role', 'phone')


class CompanySerializer(serializers.ModelSerializer):
    recruiter_name = serializers.CharField(source='recruiter.get_full_name', read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'website', 'location', 'industry', 'logo', 'is_approved', 'recruiter_name')
        read_only_fields = ('is_approved',)


class CandidateProfileSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    skills_list = serializers.ListField(source='get_skills_list', read_only=True)

    class Meta:
        model = CandidateProfile
        fields = (
            'id', 'user', 'headline', 'bio', 'skills', 'skills_list',
            'experience_years', 'education', 'resume',
            'portfolio_url', 'linkedin_url', 'github_url'
        )


class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.filter(is_approved=True),
        source='company',
        write_only=True,
        required=False
    )
    skills_list = serializers.ListField(source='get_skills_list', read_only=True)
    applicants_count = serializers.IntegerField(source='applications.count', read_only=True)

    class Meta:
        model = Job
        fields = (
            'id', 'title', 'company', 'company_id', 'description', 'responsibilities',
            'location', 'job_type', 'salary_min', 'salary_max',
            'skills_required', 'skills_list', 'experience_required_years',
            'deadline', 'is_active', 'views_count', 'applicants_count', 'created_at'
        )
        read_only_fields = ('views_count', 'created_at')


class ApplicationSerializer(serializers.ModelSerializer):
    candidate = UserPublicSerializer(read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.company.name', read_only=True)

    class Meta:
        model = Application
        fields = (
            'id', 'job', 'job_title', 'company_name', 'candidate',
            'resume', 'cover_letter', 'status', 'recruiter_notes',
            'applied_at', 'updated_at'
        )
        read_only_fields = ('applied_at', 'updated_at', 'candidate')


class SavedJobSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)

    class Meta:
        model = SavedJob
        fields = ('id', 'job', 'saved_at')
