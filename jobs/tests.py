from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import User, Company, CandidateProfile
from jobs.models import Job, Application, SavedJob


class JobPortalIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Recruiter
        self.recruiter = User.objects.create_user(
            username='recruiter_acme',
            email='recruiter@acme.com',
            password='password123',
            role=User.Role.RECRUITER
        )
        self.company = Company.objects.create(
            recruiter=self.recruiter,
            name='Acme Corp',
            location='Bengaluru, India',
            is_approved=True
        )

        # Candidate
        self.candidate = User.objects.create_user(
            username='dev_john',
            email='john@dev.com',
            password='password123',
            role=User.Role.CANDIDATE
        )
        self.profile = CandidateProfile.objects.create(
            user=self.candidate,
            headline='Django Specialist',
            skills='Python, Django, PostgreSQL, Docker'
        )

        # Job
        self.job = Job.objects.create(
            company=self.company,
            recruiter=self.recruiter,
            title='Django Backend Developer',
            description='Build REST APIs using Django and PostgreSQL.',
            location='Bengaluru',
            job_type=Job.JobType.FULL_TIME,
            salary_min=800000,
            salary_max=1400000,
            skills_required='Python, Django, PostgreSQL, AWS',
            is_active=True
        )

    def test_skill_match_percentage(self):
        candidate_skills = self.profile.get_skills_list()
        match_pct = self.job.calculate_match_percentage(candidate_skills)
        # Required skills: python, django, postgresql, aws (4)
        # Candidate has: python, django, postgresql (3 matched)
        # 3/4 = 75%
        self.assertEqual(match_pct, 75)

    def test_job_list_view(self):
        response = self.client.get(reverse('jobs:job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Backend Developer')

    def test_company_detail_view(self):
        response = self.client.get(reverse('jobs:company_detail', kwargs={'pk': self.company.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Acme Corp')
        self.assertContains(response, 'Django Backend Developer')

    def test_candidate_apply_for_job(self):
        self.client.login(username='dev_john', password='password123')
        pdf_resume = SimpleUploadedFile("my_resume.pdf", b"%PDF-1.4 test resume", content_type="application/pdf")
        
        response = self.client.post(reverse('jobs:apply_job', kwargs={'pk': self.job.pk}), {
            'resume': pdf_resume,
            'cover_letter': 'I am excited to apply for this backend developer role.'
        })

        self.assertRedirects(response, reverse('jobs:candidate_dashboard'))
        self.assertTrue(Application.objects.filter(job=self.job, candidate=self.candidate).exists())
        app = Application.objects.get(job=self.job, candidate=self.candidate)
        self.assertEqual(app.status, Application.Status.APPLIED)

    def test_prevent_duplicate_application(self):
        # Apply first time
        pdf_resume = SimpleUploadedFile("resume.pdf", b"%PDF-1.4 sample", content_type="application/pdf")
        Application.objects.create(
            job=self.job,
            candidate=self.candidate,
            resume=pdf_resume
        )

        # Try to apply again
        self.client.login(username='dev_john', password='password123')
        response = self.client.get(reverse('jobs:apply_job', kwargs={'pk': self.job.pk}))
        # Should redirect with warning message
        self.assertRedirects(response, reverse('jobs:job_detail', kwargs={'pk': self.job.pk}))

    def test_bookmark_job(self):
        self.client.login(username='dev_john', password='password123')
        response = self.client.get(reverse('jobs:toggle_save_job', kwargs={'pk': self.job.pk}))
        self.assertTrue(SavedJob.objects.filter(candidate=self.candidate, job=self.job).exists())

        # Toggle off
        response = self.client.get(reverse('jobs:toggle_save_job', kwargs={'pk': self.job.pk}))
        self.assertFalse(SavedJob.objects.filter(candidate=self.candidate, job=self.job).exists())

    def test_recruiter_status_update(self):
        pdf_resume = SimpleUploadedFile("resume.pdf", b"%PDF-1.4 sample", content_type="application/pdf")
        application = Application.objects.create(
            job=self.job,
            candidate=self.candidate,
            resume=pdf_resume,
            status=Application.Status.APPLIED
        )

        self.client.login(username='recruiter_acme', password='password123')
        response = self.client.post(reverse('jobs:recruiter_applicants', kwargs={'pk': self.job.pk}), {
            'application_id': application.id,
            'status': Application.Status.SHORTLISTED,
            'recruiter_notes': 'Strong fit for our team.'
        })

        application.refresh_from_db()
        self.assertEqual(application.status, Application.Status.SHORTLISTED)
        self.assertEqual(application.recruiter_notes, 'Strong fit for our team.')

    def test_rest_api_job_list(self):
        response = self.client.get('/api/jobs/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())
        self.assertEqual(response.json()['count'], 1)
