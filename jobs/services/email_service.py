import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def send_application_submitted_email(application):
    """
    Sends confirmation email to candidate and notification to recruiter upon application submission.
    """
    candidate = application.candidate
    job = application.job
    recruiter = job.recruiter
    company = job.company

    # 1. Email to Candidate
    candidate_subject = f"Application Received: {job.title} at {company.name}"
    candidate_message = (
        f"Hi {candidate.first_name or candidate.username},\n\n"
        f"Thank you for applying for the role of '{job.title}' at {company.name}.\n"
        f"Your application has been received and its status is currently: {application.get_status_display()}.\n\n"
        f"You can track your application status anytime from your Candidate Dashboard on CareerPulse.\n\n"
        f"Best regards,\n"
        f"The {company.name} Hiring Team"
    )

    try:
        send_mail(
            subject=candidate_subject,
            message=candidate_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[candidate.email] if candidate.email else [],
            fail_silently=True,
        )
    except Exception as e:
        logger.error(f"Error sending application email to candidate: {e}")

    # 2. Email to Recruiter
    recruiter_subject = f"New Applicant: {candidate.get_full_name() or candidate.username} applied for {job.title}"
    recruiter_message = (
        f"Hi {recruiter.first_name or recruiter.username},\n\n"
        f"A new candidate, {candidate.get_full_name() or candidate.username}, has applied for the position '{job.title}'.\n\n"
        f"Review their profile, resume, and cover letter directly from your Recruiter Dashboard.\n\n"
        f"CareerPulse Portal"
    )

    try:
        send_mail(
            subject=recruiter_subject,
            message=recruiter_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recruiter.email] if recruiter.email else [],
            fail_silently=True,
        )
    except Exception as e:
        logger.error(f"Error sending application notification to recruiter: {e}")


def send_status_update_email(application):
    """
    Sends email notification to candidate whenever application status changes (e.g. Shortlisted or Rejected).
    """
    candidate = application.candidate
    job = application.job
    company = job.company
    status = application.get_status_display()

    subject = f"Update on your application for {job.title} at {company.name}"
    
    if application.status == 'SHORTLISTED':
        body = (
            f"Dear {candidate.first_name or candidate.username},\n\n"
            f"Great news! Your application for the position '{job.title}' at {company.name} has been SHORTLISTED.\n\n"
            f"The recruiter may reach out to you directly for the next steps.\n\n"
            f"Notes from the recruiter:\n"
            f"{application.recruiter_notes or 'Your qualifications align well with our current team requirements.'}\n\n"
            f"Best wishes,\n"
            f"The {company.name} Hiring Team"
        )
    elif application.status == 'REJECTED':
        body = (
            f"Dear {candidate.first_name or candidate.username},\n\n"
            f"Thank you for taking the time to apply for '{job.title}' at {company.name}.\n\n"
            f"After careful consideration, the team has decided to proceed with other candidates whose experience "
            f"more closely matches our current needs.\n\n"
            f"We wish you all the best in your job search!\n\n"
            f"Sincerely,\n"
            f"The {company.name} Talent Acquisition Team"
        )
    else:
        body = (
            f"Dear {candidate.first_name or candidate.username},\n\n"
            f"Your application status for '{job.title}' at {company.name} is now: {status}.\n\n"
            f"Log in to CareerPulse to view your updated status."
        )

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[candidate.email] if candidate.email else [],
            fail_silently=True,
        )
    except Exception as e:
        logger.error(f"Error sending status update email to candidate: {e}")
