from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_pdf_extension, validate_file_size


class User(AbstractUser):
    class Role(models.TextChoices):
        CANDIDATE = 'candidate', 'Candidate'
        RECRUITER = 'recruiter', 'Recruiter'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CANDIDATE,
        help_text="Role determining user permissions in the portal"
    )
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_candidate(self):
        return self.role == self.Role.CANDIDATE

    @property
    def is_recruiter(self):
        return self.role == self.Role.RECRUITER

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def __str__(self):
        full_name = self.get_full_name()
        return f"{full_name or self.username} ({self.get_role_display()})"


class Company(models.Model):
    class CompanyType(models.TextChoices):
        PRODUCT = 'PRODUCT', 'Product Based'
        SERVICE = 'SERVICE', 'Service Based'
        STARTUP = 'STARTUP', 'Startup'
        MID_SIZED = 'MID_SIZED', 'Mid-sized'

    recruiter = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='company',
        limit_choices_to={'role': User.Role.RECRUITER}
    )
    name = models.CharField(max_length=255)
    company_type = models.CharField(
        max_length=20,
        choices=CompanyType.choices,
        default=CompanyType.PRODUCT,
        help_text="Product, Service, Startup, or Mid-sized company"
    )
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255, help_text="e.g. Bangalore, India or Remote")
    industry = models.CharField(max_length=100, blank=True, help_text="e.g. FinTech, SaaS, Healthcare")
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    is_approved = models.BooleanField(
        default=False,
        help_text="Designates whether the company is verified and allowed to post jobs."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def website_url(self):
        if not self.website:
            return ''
        url = self.website.strip()
        if url.startswith(('http://', 'https://')):
            return url
        return f'https://{url}'


class CandidateProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='candidate_profile',
        limit_choices_to={'role': User.Role.CANDIDATE}
    )
    headline = models.CharField(
        max_length=255,
        blank=True,
        help_text="e.g. Full Stack Python / Django Developer"
    )
    bio = models.TextField(blank=True)
    skills = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated skills (e.g. Python, Django, React, PostgreSQL)"
    )
    experience_years = models.PositiveIntegerField(default=0)
    education = models.CharField(max_length=255, blank=True)
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True,
        validators=[validate_pdf_extension, validate_file_size],
        help_text="Upload your resume in PDF format (max 5MB)"
    )
    portfolio_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_skills_list(self):
        if not self.skills:
            return []
        return [s.strip().lower() for s in self.skills.split(',') if s.strip()]

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"
