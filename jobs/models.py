from django.db import models
from django.conf import settings
from accounts.models import Company
from accounts.validators import validate_pdf_extension, validate_file_size


class Job(models.Model):
    class JobType(models.TextChoices):
        FULL_TIME = 'FULL_TIME', 'Full-time'
        PART_TIME = 'PART_TIME', 'Part-time'
        CONTRACT = 'CONTRACT', 'Contract'
        INTERNSHIP = 'INTERNSHIP', 'Internship'
        REMOTE = 'REMOTE', 'Remote'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posted_jobs'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    responsibilities = models.TextField(blank=True, help_text="Bullet points or key tasks")
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JobType.choices, default=JobType.FULL_TIME)
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    skills_required = models.CharField(
        max_length=500,
        help_text="Comma-separated skills (e.g. Python, Django, React, SQL)"
    )
    experience_required_years = models.PositiveIntegerField(
        default=0,
        help_text="Minimum years of experience required"
    )
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    def get_skills_list(self):
        if not self.skills_required:
            return []
        return [s.strip().lower() for s in self.skills_required.split(',') if s.strip()]

    def calculate_match_percentage(self, candidate_skills):
        """
        Calculate match percentage based on required skills vs candidate skills.
        Supports skill synonyms and equivalents (e.g. MySQL <-> SQL <-> PostgreSQL).
        """
        job_skills = self.get_skills_list()
        if not job_skills:
            return 100
        candidate_skills_set = set(s.strip().lower() for s in candidate_skills)

        # Equivalences & synonyms
        database_skills = {'sql', 'mysql', 'postgresql', 'postgres', 'sqlite', 'rdbms', 'relational database'}
        equivalences = {
            'sql': database_skills,
            'mysql': database_skills,
            'postgresql': database_skills,
            'postgres': database_skills,
            'sqlite': database_skills,
            'js': {'javascript', 'js'},
            'javascript': {'javascript', 'js'},
            'rest api': {'rest api', 'rest', 'api', 'drf', 'apis', 'restful'},
            'api': {'rest api', 'rest', 'api', 'drf', 'apis', 'restful'},
            'rest': {'rest api', 'rest', 'api', 'drf', 'apis', 'restful'},
            'drf': {'rest api', 'rest', 'api', 'drf', 'django rest framework'},
            'html': {'html', 'html5'},
            'html5': {'html', 'html5'},
            'css': {'css', 'css3', 'bootstrap', 'tailwind'},
            'css3': {'css', 'css3', 'bootstrap', 'tailwind'},
            'bootstrap': {'bootstrap', 'css', 'css3'},
            'git': {'git', 'github', 'version control'},
        }

        matched_count = 0
        for req in job_skills:
            req_equiv = equivalences.get(req, {req})
            # Check direct match or equivalence match
            if req_equiv.intersection(candidate_skills_set):
                matched_count += 1
            elif any(req in c or c in req for c in candidate_skills_set):
                matched_count += 1

        return int((matched_count / len(job_skills)) * 100)


class Application(models.Model):
    class Status(models.TextChoices):
        APPLIED = 'APPLIED', 'Applied'
        SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
        REJECTED = 'REJECTED', 'Rejected'

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )
    resume = models.FileField(
        upload_to='application_resumes/',
        validators=[validate_pdf_extension, validate_file_size],
        help_text="Resume submitted for this specific application (PDF max 5MB)"
    )
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.APPLIED)
    recruiter_notes = models.TextField(blank=True, help_text="Internal feedback for this candidate")
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_at']
        constraints = [
            models.UniqueConstraint(fields=['job', 'candidate'], name='unique_job_application')
        ]

    def __str__(self):
        return f"{self.candidate.get_full_name() or self.candidate.username} - {self.job.title} ({self.get_status_display()})"


class SavedJob(models.Model):
    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_jobs'
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-saved_at']
        constraints = [
            models.UniqueConstraint(fields=['candidate', 'job'], name='unique_candidate_saved_job')
        ]

    def __str__(self):
        return f"{self.candidate.username} saved {self.job.title}"
