from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    CandidateRegistrationForm,
    RecruiterRegistrationForm,
    LoginForm,
    CandidateProfileForm,
    CompanyProfileForm,
)
from .models import CandidateProfile, Company
from .decorators import candidate_required, recruiter_required


def register_candidate(request):
    if request.user.is_authenticated:
        return redirect('jobs:job_list')

    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to CareerPulse, {user.first_name or user.username}! Your candidate account has been created.")
            return redirect('accounts:candidate_profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CandidateRegistrationForm()

    return render(request, 'accounts/register_candidate.html', {'form': form})


def register_recruiter(request):
    if request.user.is_authenticated:
        return redirect('jobs:job_list')

    if request.method == 'POST':
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"Welcome, {user.first_name or user.username}! Your recruiter account and company registration have been submitted. "
                "Once approved by an admin, you can start posting jobs."
            )
            return redirect('jobs:recruiter_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RecruiterRegistrationForm()

    return render(request, 'accounts/register_recruiter.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('jobs:job_list')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if user.is_recruiter:
                return redirect('jobs:recruiter_dashboard')
            elif user.is_candidate:
                return redirect('jobs:candidate_dashboard')
            return redirect('jobs:job_list')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('jobs:job_list')


@candidate_required
def candidate_profile(request):
    profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('accounts:candidate_profile')
        else:
            messages.error(request, "There was an error updating your profile.")
    else:
        form = CandidateProfileForm(instance=profile)

    return render(request, 'accounts/candidate_profile.html', {
        'form': form,
        'profile': profile
    })


@recruiter_required
def company_profile(request):
    company = getattr(request.user, 'company', None)
    if not company:
        messages.error(request, "No company registered for this account.")
        return redirect('jobs:recruiter_dashboard')

    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Company details updated successfully!")
            return redirect('accounts:company_profile')
        else:
            messages.error(request, "There was an error updating your company profile.")
    else:
        form = CompanyProfileForm(instance=company)

    return render(request, 'accounts/company_profile.html', {
        'form': form,
        'company': company
    })
