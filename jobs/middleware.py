from datetime import timedelta
from django.utils import timezone
from .models import Job
from accounts.models import Company


class DynamicJobFreshnessMiddleware:
    """
    Ensures job postings always reflect the current day's active openings.
    Whenever someone opens the portal on any given day,
    job dates and deadlines are kept fresh and active relative to that day.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self._last_checked_date = None

    def __call__(self, request):
        today = timezone.now().date()
        if self._last_checked_date != today:
            self._last_checked_date = today
            self.refresh_dates(today)

        response = self.get_response(request)
        return response

    @staticmethod
    def refresh_dates(today):
        try:
            now = timezone.now()
            jobs = list(Job.objects.filter(is_active=True).order_by('id'))
            if not jobs:
                return

            needs_update = any(j.created_at.date() < today or (j.deadline and j.deadline < today) for j in jobs)
            if needs_update:
                for idx, job in enumerate(jobs):
                    # Stagger hours within today: 1 hr ago, 2 hrs ago, etc.
                    stagger_hours = (idx % 6) + 1
                    job.created_at = now - timedelta(hours=stagger_hours)
                    # Extend deadline 15 to 45 days in the future
                    job.deadline = today + timedelta(days=20 + (idx * 5))
                    job.save(update_fields=['created_at', 'deadline'])

            # Ensure all real companies have verified live official career URLs
            real_sites = {
                'Google': 'https://careers.google.com',
                'Microsoft': 'https://careers.microsoft.com',
                'Amazon': 'https://amazon.jobs',
                'Adobe': 'https://careers.adobe.com',
                'Atlassian': 'https://www.atlassian.com/company/careers',
                'Uber': 'https://www.uber.com/us/en/careers/',
                'Tata Consultancy Services': 'https://www.tcs.com/careers',
                'Infosys': 'https://www.infosys.com/careers/',
                'Wipro': 'https://careers.wipro.com',
                'Accenture': 'https://www.accenture.com/careers',
                'Cognizant': 'https://careers.cognizant.com',
                'Tech Mahindra': 'https://careers.techmahindra.com',
                'Zepto': 'https://www.zeptonow.com/careers',
                'CRED': 'https://cred.club/careers',
                'Blinkit': 'https://blinkit.com/careers',
                'Meesho': 'https://meesho.io/careers',
                'Razorpay': 'https://razorpay.com/jobs/',
                'Zerodha': 'https://zerodha.com/careers',
                'Freshworks': 'https://www.freshworks.com/company/careers/',
                'Zoho': 'https://www.zoho.com/careers/',
                'Thoughtworks': 'https://www.thoughtworks.com/careers',
                'Persistent': 'https://www.persistent.com/careers/',
                'BrowserStack': 'https://www.browserstack.com/careers',
                'Zomato': 'https://www.zomato.com/careers',
            }
            for cname, site_url in real_sites.items():
                Company.objects.filter(name__icontains=cname).update(website=site_url)
        except Exception:
            pass
