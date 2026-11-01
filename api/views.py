from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404

from jobs.models import Job, Application, SavedJob
from accounts.models import CandidateProfile, Company
from .serializers import (
    JobSerializer,
    ApplicationSerializer,
    CandidateProfileSerializer,
    CompanySerializer,
    SavedJobSerializer
)
from jobs.services.email_service import send_application_submitted_email, send_status_update_email


class IsRecruiterOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_recruiter

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.recruiter == request.user


class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, searching, creating, and updating job postings.
    """
    queryset = Job.objects.filter(is_active=True, company__is_approved=True).select_related('company', 'recruiter')
    serializer_class = JobSerializer
    permission_classes = [IsRecruiterOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.query_params.get('q', None)
        location = self.request.query_params.get('location', None)
        job_type = self.request.query_params.get('job_type', None)

        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(skills_required__icontains=query) |
                Q(company__name__icontains=query)
            )
        if location:
            qs = qs.filter(location__icontains=location)
        if job_type:
            qs = qs.filter(job_type=job_type)
        return qs

    def perform_create(self, serializer):
        company = getattr(self.request.user, 'company', None)
        if not company or not company.is_approved:
            raise permissions.exceptions.PermissionDenied("You must have an approved company to post jobs.")
        serializer.save(recruiter=self.request.user, company=company)


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Job Applications.
    Candidates can view their submissions and apply.
    Recruiters can view applications for their jobs and update status.
    """
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_recruiter:
            return Application.objects.filter(job__recruiter=user).select_related('job', 'candidate', 'job__company')
        elif user.is_candidate:
            return Application.objects.filter(candidate=user).select_related('job', 'job__company')
        elif user.is_superuser:
            return Application.objects.all().select_related('job', 'candidate')
        return Application.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_candidate:
            raise permissions.exceptions.PermissionDenied("Only candidates can apply for jobs.")
        application = serializer.save(candidate=user)
        send_application_submitted_email(application)

    def perform_update(self, serializer):
        old_status = self.get_object().status
        application = serializer.save()
        if old_status != application.status:
            send_status_update_email(application)


class RecruiterAnalyticsAPIView(APIView):
    """
    Returns analytics for the logged-in recruiter:
    - Applications per job
    - Status breakdown (Applied, Shortlisted, Rejected)
    - Total views
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_recruiter:
            return Response({'error': 'Recruiter access only'}, status=status.HTTP_403_FORBIDDEN)

        jobs = Job.objects.filter(recruiter=request.user).annotate(
            total_apps=Count('applications'),
            shortlisted_apps=Count('applications', filter=Q(applications__status=Application.Status.SHORTLISTED)),
            rejected_apps=Count('applications', filter=Q(applications__status=Application.Status.REJECTED)),
        )

        job_analytics = [
            {
                'id': j.id,
                'title': j.title,
                'views': j.views_count,
                'total_applications': j.total_apps,
                'shortlisted': j.shortlisted_apps,
                'rejected': j.rejected_apps,
                'pending': j.total_apps - (j.shortlisted_apps + j.rejected_apps),
            }
            for j in jobs
        ]

        total_applications = sum(item['total_applications'] for item in job_analytics)
        total_shortlisted = sum(item['shortlisted'] for item in job_analytics)

        return Response({
            'total_jobs_posted': jobs.count(),
            'total_applications_received': total_applications,
            'total_shortlisted': total_shortlisted,
            'shortlist_rate_percentage': round((total_shortlisted / total_applications * 100), 1) if total_applications else 0,
            'jobs': job_analytics
        })
