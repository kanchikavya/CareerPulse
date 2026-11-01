from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import User

def candidate_required(view_func):
    """
    Decorator for views that checks that the logged-in user is a Candidate.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to access this page.")
            return redirect('accounts:login')
        if not request.user.is_candidate:
            messages.error(request, "Access restricted to candidates only.")
            return redirect('jobs:job_list')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def recruiter_required(view_func):
    """
    Decorator for views that checks that the logged-in user is a Recruiter.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in as a recruiter to access this page.")
            return redirect('accounts:login')
        if not request.user.is_recruiter:
            messages.error(request, "Access restricted to recruiters only.")
            return redirect('jobs:job_list')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def approved_recruiter_required(view_func):
    """
    Decorator checking that the recruiter's company has been approved by admin.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in as a recruiter to access this page.")
            return redirect('accounts:login')
        if not request.user.is_recruiter:
            messages.error(request, "Access restricted to recruiters only.")
            return redirect('jobs:job_list')
        
        company = getattr(request.user, 'company', None)
        if not company or not company.is_approved:
            messages.warning(
                request,
                "Your company profile is pending approval by the portal administrator. "
                "Once approved, you can post and manage jobs."
            )
            return redirect('jobs:recruiter_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
