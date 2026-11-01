from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone

from .models import Job, Application, SavedJob
from .forms import JobForm, ApplicationForm, ApplicationStatusForm
from accounts.models import Company, CandidateProfile
from accounts.decorators import candidate_required, recruiter_required, approved_recruiter_required
from .services.email_service import send_application_submitted_email, send_status_update_email
from .services.ats_service import analyze_resume_ats, extract_text_from_pdf_bytes


def home_view(request):
    """
    Public landing page with search bar, metrics, category tabs, and featured active jobs.
    """
    recent_jobs = (
        Job.objects.filter(is_active=True, company__is_approved=True)
        .select_related('company')
        .order_by('-created_at')[:9]
    )
    total_jobs = Job.objects.filter(is_active=True).count()
    total_companies = Company.objects.filter(is_approved=True).count()
    total_applications = Application.objects.count()

    # Featured companies by type
    featured_companies = Company.objects.filter(is_approved=True).annotate(
        openings_count=Count('jobs', filter=Q(jobs__is_active=True))
    ).order_by('-openings_count')[:12]

    context = {
        'recent_jobs': recent_jobs,
        'total_jobs': total_jobs,
        'total_companies': total_companies,
        'total_applications': total_applications,
        'featured_companies': featured_companies,
        'company_type_choices': Company.CompanyType.choices,
    }
    return render(request, 'home.html', context)


def company_list_view(request):
    """
    Public directory of verified companies categorized by:
    Product Based, Service Based, Startups, and Mid-sized.
    """
    company_type = request.GET.get('type', '').strip()
    query = request.GET.get('q', '').strip()

    companies = Company.objects.filter(is_approved=True).annotate(
        openings_count=Count('jobs', filter=Q(jobs__is_active=True))
    ).order_by('name')

    if company_type:
        companies = companies.filter(company_type=company_type)

    if query:
        companies = companies.filter(
            Q(name__icontains=query) |
            Q(industry__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query)
        )

    # Counts for each category tab
    all_approved = Company.objects.filter(is_approved=True)
    counts = {
        'ALL': all_approved.count(),
        'PRODUCT': all_approved.filter(company_type=Company.CompanyType.PRODUCT).count(),
        'SERVICE': all_approved.filter(company_type=Company.CompanyType.SERVICE).count(),
        'STARTUP': all_approved.filter(company_type=Company.CompanyType.STARTUP).count(),
        'MID_SIZED': all_approved.filter(company_type=Company.CompanyType.MID_SIZED).count(),
    }

    context = {
        'companies': companies,
        'selected_type': company_type,
        'query': query,
        'counts': counts,
        'company_type_choices': Company.CompanyType.choices,
    }
    return render(request, 'jobs/company_list.html', context)


def company_detail_view(request, pk):
    """
    Public company information page:
    Shows comprehensive company background, industry, headquarters,
    mission, perks, and all active job openings from this company.
    """
    company = get_object_or_404(Company, pk=pk, is_approved=True)
    active_jobs = company.jobs.filter(is_active=True).order_by('-created_at')

    candidate_skills = []
    if request.user.is_authenticated and request.user.is_candidate:
        profile = getattr(request.user, 'candidate_profile', None)
        if profile:
            candidate_skills = profile.get_skills_list()

    job_items = []
    for job in active_jobs:
        match_pct = job.calculate_match_percentage(candidate_skills) if candidate_skills else None
        job_items.append({
            'job': job,
            'match_pct': match_pct,
        })

    context = {
        'company': company,
        'job_items': job_items,
        'total_openings': active_jobs.count(),
    }
    return render(request, 'jobs/company_detail.html', context)


def job_list_view(request):
    """
    Search & Filter jobs with pagination and skill match calculations.
    Optimized with select_related for high performance.
    """
    query = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()
    job_type = request.GET.get('job_type', '').strip()
    company_type = request.GET.get('company_type', '').strip()
    min_salary = request.GET.get('min_salary', '').strip()

    jobs = (
        Job.objects.filter(is_active=True, company__is_approved=True)
        .select_related('company', 'recruiter')
    )

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(skills_required__icontains=query) |
            Q(company__name__icontains=query)
        )

    if location:
        jobs = jobs.filter(location__icontains=location)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    if company_type:
        jobs = jobs.filter(company__company_type=company_type)

    if min_salary and min_salary.isdigit():
        jobs = jobs.filter(salary_max__gte=int(min_salary))

    # Skill match & saved job tracking for candidate
    saved_job_ids = set()
    candidate_skills = []
    if request.user.is_authenticated and request.user.is_candidate:
        saved_job_ids = set(
            SavedJob.objects.filter(candidate=request.user).values_list('job_id', flat=True)
        )
        profile = getattr(request.user, 'candidate_profile', None)
        if profile:
            candidate_skills = profile.get_skills_list()

    # Calculate skill matches for each job
    job_items = []
    for job in jobs:
        match_pct = job.calculate_match_percentage(candidate_skills) if candidate_skills else None
        job_items.append({
            'job': job,
            'is_saved': job.id in saved_job_ids,
            'match_pct': match_pct,
        })

    paginator = Paginator(job_items, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'location': location,
        'job_type': job_type,
        'company_type': company_type,
        'min_salary': min_salary,
        'job_type_choices': Job.JobType.choices,
        'company_type_choices': Company.CompanyType.choices,
        'total_count': paginator.count,
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail_view(request, pk):
    """
    Detailed job view with company overview, applicant status, and bookmark status.
    """
    job = get_object_or_404(
        Job.objects.select_related('company', 'recruiter'),
        pk=pk
    )

    # Increment view count
    Job.objects.filter(pk=pk).update(views_count=job.views_count + 1)

    has_applied = False
    is_saved = False
    match_pct = None
    existing_application = None

    if request.user.is_authenticated and request.user.is_candidate:
        existing_application = Application.objects.filter(job=job, candidate=request.user).first()
        has_applied = existing_application is not None
        is_saved = SavedJob.objects.filter(job=job, candidate=request.user).exists()

        profile = getattr(request.user, 'candidate_profile', None)
        if profile:
            match_pct = job.calculate_match_percentage(profile.get_skills_list())

    # Related jobs (same company or similar title)
    related_jobs = (
        Job.objects.filter(is_active=True, company__is_approved=True)
        .exclude(pk=job.pk)
        .filter(Q(company=job.company) | Q(job_type=job.job_type))
        .select_related('company')[:3]
    )

    context = {
        'job': job,
        'has_applied': has_applied,
        'existing_application': existing_application,
        'is_saved': is_saved,
        'match_pct': match_pct,
        'related_jobs': related_jobs,
    }
    return render(request, 'jobs/job_detail.html', context)


@approved_recruiter_required
def job_create_view(request):
    """
    Recruiter creates a new job posting.
    """
    company = request.user.company

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.recruiter = request.user
            job.save()
            messages.success(request, f"Job '{job.title}' posted successfully!")
            return redirect('jobs:job_detail', pk=job.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = JobForm()

    return render(request, 'jobs/job_form.html', {
        'form': form,
        'title': 'Post a New Job',
        'company': company,
    })


@recruiter_required
def job_update_view(request, pk):
    """
    Recruiter updates an existing job posting.
    """
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f"Job '{job.title}' updated successfully!")
            return redirect('jobs:job_detail', pk=job.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/job_form.html', {
        'form': form,
        'title': f"Edit: {job.title}",
        'job': job,
    })


@recruiter_required
def job_delete_view(request, pk):
    """
    Recruiter deletes or deactivates a job posting.
    """
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)

    if request.method == 'POST':
        job_title = job.title
        job.delete()
        messages.success(request, f"Job '{job_title}' was permanently deleted.")
        return redirect('jobs:recruiter_dashboard')

    return render(request, 'jobs/job_confirm_delete.html', {'job': job})


@candidate_required
def apply_job_view(request, pk):
    """
    Candidate applies to a job with resume PDF and optional cover letter.
    """
    job = get_object_or_404(Job, pk=pk, is_active=True, company__is_approved=True)
    profile = getattr(request.user, 'candidate_profile', None)

    # Check if deadline passed
    if job.deadline and job.deadline < timezone.now().date():
        messages.error(request, "The deadline for this job posting has already passed.")
        return redirect('jobs:job_detail', pk=job.pk)

    # Check if already applied
    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.warning(request, "You have already applied for this position.")
        return redirect('jobs:job_detail', pk=job.pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, candidate_profile=profile)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user

            # If user checked "use profile resume", copy resume from profile
            if form.cleaned_data.get('use_profile_resume') and profile and profile.resume:
                application.resume = profile.resume

            application.save()

            # Trigger automated notification emails
            send_application_submitted_email(application)

            messages.success(request, f"Application submitted successfully for '{job.title}'!")
            return redirect('jobs:candidate_dashboard')
        else:
            messages.error(request, "Please correct the errors in your submission.")
    else:
        form = ApplicationForm(candidate_profile=profile)

    return render(request, 'jobs/apply_job.html', {
        'form': form,
        'job': job,
        'profile': profile,
    })


@login_required
def toggle_save_job(request, pk):
    """
    Toggle bookmark on a job (AJAX or standard POST/GET).
    """
    if not request.user.is_candidate:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Only candidates can save jobs.'}, status=403)
        messages.error(request, "Only candidates can save jobs.")
        return redirect('jobs:job_detail', pk=pk)

    job = get_object_or_404(Job, pk=pk)
    saved_job = SavedJob.objects.filter(candidate=request.user, job=job).first()

    if saved_job:
        saved_job.delete()
        is_saved = False
        msg = f"Removed '{job.title}' from your saved jobs."
    else:
        SavedJob.objects.create(candidate=request.user, job=job)
        is_saved = True
        msg = f"Saved '{job.title}' to your bookmarks!"

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', 'is_saved': is_saved, 'message': msg})

    messages.info(request, msg)
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('jobs:job_detail', pk=pk)


@candidate_required
def candidate_dashboard_view(request):
    """
    Candidate Dashboard: Application tracker, saved jobs, and skill recommendations.
    """
    user = request.user
    applications = (
        Application.objects.filter(candidate=user)
        .select_related('job', 'job__company')
        .order_by('-applied_at')
    )

    saved_jobs = (
        SavedJob.objects.filter(candidate=user)
        .select_related('job', 'job__company')
        .order_by('-saved_at')
    )

    profile = getattr(user, 'candidate_profile', None)
    candidate_skills = profile.get_skills_list() if profile else []

    # Skill-based Job Recommendations
    recommended_jobs = []
    suggested_roles = []
    if candidate_skills:
        c_set = set(candidate_skills)
        if {'python', 'django'}.intersection(c_set):
            if {'react', 'javascript'}.intersection(c_set) and {'mysql', 'sql'}.intersection(c_set):
                suggested_roles.append({
                    'title': 'Full Stack Python Developer',
                    'match_rate': '95%',
                    'description': 'Build end-to-end web apps combining Django backend, React frontend, and MySQL database.',
                    'primary_skills': 'Python, Django, React, MySQL, JavaScript, HTML/CSS',
                    'tag': 'Top Match'
                })
            if {'mysql', 'sql'}.intersection(c_set):
                suggested_roles.append({
                    'title': 'Backend Developer (Python & MySQL)',
                    'match_rate': '92%',
                    'description': 'Develop business logic, REST APIs, models, migrations, and database queries in MySQL.',
                    'primary_skills': 'Python, Django, MySQL, REST APIs, SQL Queries, Git',
                    'tag': 'High Demand'
                })
            suggested_roles.append({
                'title': 'Junior Python / Django Developer',
                'match_rate': '90%',
                'description': 'Develop web applications, user authentication, views, templates, and CRUD operations.',
                'primary_skills': 'Python, Django, HTML, CSS, Bootstrap, Relational DB',
                'tag': 'Entry / Mid'
            })
            suggested_roles.append({
                'title': 'Associate Software Engineer',
                'match_rate': '85%',
                'description': 'Enterprise software development at top product giants and premier IT service leaders.',
                'primary_skills': 'Python, OOP, SQL/MySQL, Data Structures, Git',
                'tag': 'Versatile'
            })

        active_jobs = (
            Job.objects.filter(is_active=True, company__is_approved=True)
            .exclude(applications__candidate=user)
            .select_related('company')
        )
        scored_jobs = []
        for j in active_jobs:
            score = j.calculate_match_percentage(candidate_skills)
            if score > 0:
                scored_jobs.append((score, j))
        # Sort descending by match score
        scored_jobs.sort(key=lambda x: x[0], reverse=True)
        recommended_jobs = [{'job': j, 'match_pct': score} for score, j in scored_jobs[:9]]

    # Statistics
    total_applied = applications.count()
    shortlisted_count = applications.filter(status=Application.Status.SHORTLISTED).count()
    rejected_count = applications.filter(status=Application.Status.REJECTED).count()
    pending_count = applications.filter(status=Application.Status.APPLIED).count()

    context = {
        'profile': profile,
        'applications': applications,
        'saved_jobs': saved_jobs,
        'recommended_jobs': recommended_jobs,
        'suggested_roles': suggested_roles,
        'total_applied': total_applied,
        'shortlisted_count': shortlisted_count,
        'rejected_count': rejected_count,
        'pending_count': pending_count,
    }
    return render(request, 'jobs/candidate_dashboard.html', context)


@recruiter_required
def recruiter_dashboard_view(request):
    """
    Recruiter Dashboard: Analytics, active postings, total applicant counts.
    """
    company = getattr(request.user, 'company', None)
    jobs = (
        Job.objects.filter(recruiter=request.user)
        .annotate(
            applicant_count=Count('applications'),
            shortlisted_count=Count('applications', filter=Q(applications__status=Application.Status.SHORTLISTED)),
            rejected_count=Count('applications', filter=Q(applications__status=Application.Status.REJECTED)),
        )
        .order_by('-created_at')
    )

    total_jobs = jobs.count()
    total_applicants = Application.objects.filter(job__recruiter=request.user).count()
    total_shortlisted = Application.objects.filter(
        job__recruiter=request.user,
        status=Application.Status.SHORTLISTED
    ).count()

    context = {
        'company': company,
        'jobs': jobs,
        'total_jobs': total_jobs,
        'total_applicants': total_applicants,
        'total_shortlisted': total_shortlisted,
    }
    return render(request, 'jobs/recruiter_dashboard.html', context)


@recruiter_required
def recruiter_job_applicants_view(request, pk):
    """
    Recruiter reviews all applicants for a specific job, filters by status,
    and updates application status with optional feedback notes.
    """
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)
    status_filter = request.GET.get('status', '').strip()

    applicants_qs = (
        Application.objects.filter(job=job)
        .select_related('candidate', 'candidate__candidate_profile')
        .order_by('-applied_at')
    )

    if status_filter in dict(Application.Status.choices):
        applicants_qs = applicants_qs.filter(status=status_filter)

    # Compute match percentage for each applicant
    job_skills = set(job.get_skills_list())
    applicant_list = []
    for app in applicants_qs:
        candidate_profile = getattr(app.candidate, 'candidate_profile', None)
        c_skills = candidate_profile.get_skills_list() if candidate_profile else []
        matched = job_skills.intersection(set(c_skills)) if job_skills else set()
        match_pct = int((len(matched) / len(job_skills)) * 100) if job_skills else 100
        applicant_list.append({
            'app': app,
            'profile': candidate_profile,
            'match_pct': match_pct,
        })

    # Status update handler
    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        notes = request.POST.get('recruiter_notes', '')

        application = get_object_or_404(Application, pk=app_id, job=job)
        if new_status in dict(Application.Status.choices):
            old_status = application.status
            application.status = new_status
            application.recruiter_notes = notes
            application.save()

            # Send email notification if status changed
            if old_status != new_status:
                send_status_update_email(application)

            messages.success(
                request,
                f"Updated status for {application.candidate.get_full_name() or application.candidate.username} to {application.get_status_display()}."
            )
            return redirect('jobs:recruiter_applicants', pk=job.pk)

    context = {
        'job': job,
        'applicant_list': applicant_list,
        'current_status': status_filter,
        'status_choices': Application.Status.choices,
        'total_applicants': job.applications.count(),
    }
    return render(request, 'jobs/recruiter_applicants.html', context)


def ats_checker_view(request, job_id=None):
    """
    ATS (Applicant Tracking System) Resume Scanner & Tailoring Assistant.
    Evaluates candidate resume against target job requirements, calculates ATS match score (0-100),
    identifies missing keywords, checks structural health, and provides tailored suggestions.
    """
    active_jobs = Job.objects.filter(is_active=True, company__is_approved=True).select_related('company').order_by('-created_at')

    selected_job = None
    if job_id:
        selected_job = get_object_or_404(Job, pk=job_id, is_active=True)
    elif active_jobs.exists():
        selected_job = active_jobs.first()

    profile = None
    if request.user.is_authenticated and request.user.is_candidate:
        profile = getattr(request.user, 'candidate_profile', None)

    analysis_result = None
    resume_text = ""
    resume_source = request.POST.get('resume_source', 'profile' if (profile and profile.skills) else 'paste')

    if request.method == 'POST':
        target_job_id = request.POST.get('target_job_id')
        if target_job_id:
            selected_job = get_object_or_404(Job, pk=target_job_id, is_active=True)

        if resume_source == 'paste':
            resume_text = request.POST.get('resume_text', '').strip()
        elif resume_source == 'upload' and 'resume_file' in request.FILES:
            uploaded_file = request.FILES['resume_file']
            file_bytes = uploaded_file.read()
            if uploaded_file.name.lower().endswith('.pdf'):
                resume_text = extract_text_from_pdf_bytes(file_bytes)
            else:
                resume_text = file_bytes.decode('utf-8', errors='ignore')
        else:
            if profile:
                parts = [
                    profile.user.get_full_name(),
                    profile.headline,
                    profile.bio,
                    f"Technical Skills: {profile.skills}",
                    f"Experience: {profile.experience_years} years",
                    f"Education: {profile.education}",
                ]
                if profile.resume:
                    try:
                        profile.resume.open('rb')
                        pbytes = profile.resume.read()
                        extracted = extract_text_from_pdf_bytes(pbytes)
                        if extracted:
                            parts.append(extracted)
                    except Exception:
                        pass
                resume_text = "\n".join([p for p in parts if p])

        if selected_job and resume_text:
            analysis_result = analyze_resume_ats(resume_text, selected_job)
        elif selected_job and not resume_text:
            messages.warning(request, "Please enter or upload resume content to analyze.")

    # Default initial analysis if candidate visits with saved profile
    elif selected_job and profile and profile.skills:
        profile_parts = [
            profile.user.get_full_name(),
            profile.headline,
            profile.bio,
            f"Technical Skills: {profile.skills}",
            f"Experience: {profile.experience_years} years",
            f"Education: {profile.education}",
        ]
        resume_text = "\n".join([p for p in profile_parts if p])
        analysis_result = analyze_resume_ats(resume_text, selected_job)

    context = {
        'active_jobs': active_jobs,
        'selected_job': selected_job,
        'profile': profile,
        'resume_text': resume_text,
        'resume_source': resume_source,
        'analysis': analysis_result,
    }
    return render(request, 'jobs/ats_checker.html', context)
