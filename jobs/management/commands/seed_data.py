from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from accounts.models import User, Company, CandidateProfile
from jobs.models import Job, Application, SavedJob


class Command(BaseCommand):
    help = "Seeds the database with realistic sample users, companies, jobs, and applications"

    def handle(self, *args, **options):
        self.stdout.write("Seeding sample data...")

        # 1. Admin User
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@careerpulse.dev',
                'first_name': 'System',
                'last_name': 'Administrator',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))

        # 2. Recruiters & Real Companies
        recruiter_google, _ = User.objects.get_or_create(
            username='recruiter_google',
            defaults={
                'email': 'careers@google.com',
                'first_name': 'Sundar',
                'last_name': 'Hiring Team',
                'role': User.Role.RECRUITER,
                'phone': '+91 98765 43210'
            }
        )
        recruiter_google.set_password('password123')
        recruiter_google.save()

        company_google, _ = Company.objects.get_or_create(
            recruiter=recruiter_google,
            defaults={
                'name': 'Google',
                'description': 'Google is a global technology leader focused on organizing the world information and making it universally accessible and useful. Google engineering centers in India build world-class products across Search, Cloud, Android, YouTube, and AI platforms.',
                'website': 'https://careers.google.com',
                'location': 'Bengaluru & Hyderabad, India (Hybrid)',
                'industry': 'Software, Cloud & Artificial Intelligence',
                'is_approved': True,
            }
        )

        recruiter_razorpay, _ = User.objects.get_or_create(
            username='recruiter_razorpay',
            defaults={
                'email': 'talent@razorpay.com',
                'first_name': 'Harshil',
                'last_name': 'Hiring Team',
                'role': User.Role.RECRUITER,
                'phone': '+91 91234 56789'
            }
        )
        recruiter_razorpay.set_password('password123')
        recruiter_razorpay.save()

        company_razorpay, _ = Company.objects.get_or_create(
            recruiter=recruiter_razorpay,
            defaults={
                'name': 'Razorpay',
                'description': 'Razorpay is India premier full-stack financial solutions platform, empowering millions of businesses to accept, process, and disburse digital payments via developer-friendly APIs.',
                'website': 'https://razorpay.com/jobs/',
                'location': 'Bengaluru, India',
                'industry': 'FinTech & Payment Infrastructure',
                'is_approved': True,
            }
        )

        recruiter_microsoft, _ = User.objects.get_or_create(
            username='recruiter_microsoft',
            defaults={
                'email': 'careers@microsoft.com',
                'first_name': 'Satya',
                'last_name': 'Talent Acquisition',
                'role': User.Role.RECRUITER,
                'phone': '+91 99887 11223'
            }
        )
        recruiter_microsoft.set_password('password123')
        recruiter_microsoft.save()

        company_microsoft, _ = Company.objects.get_or_create(
            recruiter=recruiter_microsoft,
            defaults={
                'name': 'Microsoft',
                'description': 'Microsoft enables digital transformation for the era of an intelligent cloud and intelligent edge, building core Azure cloud infrastructure, AI models, and enterprise software.',
                'website': 'https://careers.microsoft.com',
                'location': 'Hyderabad & Bengaluru, India (Hybrid & Remote)',
                'industry': 'Enterprise Software & Cloud Platforms',
                'is_approved': True,
            }
        )

        # 3. Candidates
        dummy_pdf = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R>>endobj\nxref\n0 4\n0000000000 65535 f\n0000000009 00000 n\n0000000052 00000 n\n0000000108 00000 n\ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n178\n%%EOF"

        alice, created = User.objects.get_or_create(
            username='alice_dev',
            defaults={
                'email': 'alice@devmail.com',
                'first_name': 'Alice',
                'last_name': 'Sharma',
                'role': User.Role.CANDIDATE,
                'phone': '+91 99887 76655'
            }
        )
        if created:
            alice.set_password('password123')
            alice.save()

        alice_profile, _ = CandidateProfile.objects.get_or_create(
            user=alice,
            defaults={
                'headline': 'Senior Python & Django Full Stack Developer',
                'bio': 'Passionate engineer with 4 years building scalable web services, REST APIs, and event-driven backends.',
                'skills': 'Python, Django, PostgreSQL, Docker, Redis, Celery, REST API',
                'experience_years': 4,
                'education': 'B.Tech in Computer Science',
                'portfolio_url': 'https://github.com',
                'github_url': 'https://github.com/alicedev',
            }
        )
        if not alice_profile.resume:
            alice_profile.resume.save('alice_resume.pdf', ContentFile(dummy_pdf))
            alice_profile.save()

        bob, created = User.objects.get_or_create(
            username='bob_coder',
            defaults={
                'email': 'bob@devmail.com',
                'first_name': 'Bob',
                'last_name': 'Verma',
                'role': User.Role.CANDIDATE,
                'phone': '+91 97766 55443'
            }
        )
        if created:
            bob.set_password('password123')
            bob.save()

        bob_profile, _ = CandidateProfile.objects.get_or_create(
            user=bob,
            defaults={
                'headline': 'Full Stack Developer | React & Python Enthusiast',
                'bio': 'Frontend leaning engineer who loves crafting interactive UIs with React and robust backends with Django and FastAPI.',
                'skills': 'JavaScript, React, Python, Django, HTML, CSS, Bootstrap, Git',
                'experience_years': 2,
                'education': 'B.E. in Information Technology',
                'github_url': 'https://github.com/bobcoder',
            }
        )
        if not bob_profile.resume:
            bob_profile.resume.save('bob_resume.pdf', ContentFile(dummy_pdf))
            bob_profile.save()

        # 4. Jobs
        jobs_data = [
            {
                'company': company_google,
                'recruiter': recruiter_google,
                'title': 'Software Engineer, Python & Distributed Cloud',
                'description': 'As a Software Engineer at Google, you will work on our core distributed cloud systems and internal platforms that scale across millions of machines. You will write robust, high-performance Python code, develop scalable REST interfaces, and optimize large-scale data storage layers.',
                'responsibilities': '- Build and maintain multi-tenant cloud backend infrastructure in Python\n- Write clean, highly testable code adhering to Google engineering standards\n- Collaborate with cross-functional teams in Bengaluru and Sunnyvale',
                'location': 'Bengaluru, India (Hybrid)',
                'job_type': Job.JobType.FULL_TIME,
                'salary_min': 2400000,
                'salary_max': 3800000,
                'skills_required': 'Python, Django, REST API, Distributed Systems, GCP, Docker',
                'experience_required_years': 3,
                'deadline': date.today() + timedelta(days=30),
                'views_count': 142,
            },
            {
                'company': company_google,
                'recruiter': recruiter_google,
                'title': 'Backend Systems Developer (Python & GCP)',
                'description': 'Help Google Cloud deliver asynchronous task processing pipelines, event streaming integrations, and telemetry monitoring services for Google Cloud Platform.',
                'responsibilities': '- Architect event-driven worker services with Python and message queues\n- Benchmark latency, profile bottlenecks, and optimize query performance\n- Participate in on-call rotations and site reliability engineering',
                'location': 'Hyderabad, India',
                'job_type': Job.JobType.FULL_TIME,
                'salary_min': 1800000,
                'salary_max': 2800000,
                'skills_required': 'Python, Django, Celery, Redis, Linux, Cloud Architecture',
                'experience_required_years': 2,
                'deadline': date.today() + timedelta(days=45),
                'views_count': 98,
            },
            {
                'company': company_microsoft,
                'recruiter': recruiter_microsoft,
                'title': 'Full Stack Web Developer (Python + React, Azure)',
                'description': 'Microsoft is looking for a versatile Full Stack Developer to build modern cloud dashboards for enterprise Azure customers. You will combine Django REST Framework on the backend with React on the frontend.',
                'responsibilities': '- Create accessible, fast React frontend components with modern state management\n- Design secure token-based REST endpoints using DRF and Azure Active Directory\n- Partner with UX researchers and product managers on feature iterations',
                'location': 'Bengaluru, India (Hybrid & Remote)',
                'job_type': Job.JobType.FULL_TIME,
                'salary_min': 1800000,
                'salary_max': 2800000,
                'skills_required': 'Python, Django, React, TypeScript, HTML, CSS, Azure',
                'experience_required_years': 2,
                'deadline': date.today() + timedelta(days=20),
                'views_count': 210,
            },
            {
                'company': company_razorpay,
                'recruiter': recruiter_razorpay,
                'title': 'Senior Python Backend Architect (High-Scale Ledger)',
                'description': 'Lead architecture for our core double-entry accounting ledger engine handling millions of daily financial transactions. You will guarantee strict ACID compliance, sub-10ms response times, and multi-region failover.',
                'responsibilities': '- Lead ledger engine architecture and high-availability database replication\n- Mentor backend engineers on database isolation levels and lock tuning\n- Enforce financial audit logging and zero-loss architecture',
                'location': 'Bengaluru, India (Hybrid)',
                'job_type': Job.JobType.FULL_TIME,
                'salary_min': 2600000,
                'salary_max': 4200000,
                'skills_required': 'Python, Django, PostgreSQL, High-Scale, Redis, Docker',
                'experience_required_years': 5,
                'deadline': date.today() + timedelta(days=15),
                'views_count': 85,
            },
            {
                'company': company_razorpay,
                'recruiter': recruiter_razorpay,
                'title': 'Junior Software Engineer (Python / FinTech Payments)',
                'description': 'Start your fintech engineering career at India foremost payment company. Work alongside senior architects building transaction processing APIs, automated bank reconciliations, and merchant payout systems.',
                'responsibilities': '- Build and maintain REST API endpoints for merchant onboarding\n- Write comprehensive unit and regression tests in Django\n- Debug transaction edge cases and assist in developer documentation',
                'location': 'Bengaluru, India',
                'job_type': Job.JobType.INTERNSHIP,
                'salary_min': 600000,
                'salary_max': 1000000,
                'skills_required': 'Python, Django, SQL, PostgreSQL, Git, Problem Solving',
                'experience_required_years': 0,
                'deadline': date.today() + timedelta(days=60),
                'views_count': 320,
            },
            {
                'company': company_microsoft,
                'recruiter': recruiter_microsoft,
                'title': 'Software Engineer II - Cloud APIs & Microservices',
                'description': 'Design, code, and deploy resilient microservices that power enterprise Office 365 collaboration tools. You will optimize relational database schemas, write high-concurrency background processors, and maintain 99.99% uptime.',
                'responsibilities': '- Implement scalable RESTful web services in Python and Django\n- Write integration tests with pytest and automate CI/CD GitHub Actions\n- Analyze production metrics and diagnose distributed concurrency issues',
                'location': 'Hyderabad, India',
                'job_type': Job.JobType.FULL_TIME,
                'salary_min': 2000000,
                'salary_max': 3200000,
                'skills_required': 'Python, Django, PostgreSQL, Docker, Kubernetes, Microservices',
                'experience_required_years': 4,
                'deadline': date.today() + timedelta(days=25),
                'views_count': 160,
            },
        ]

        created_jobs = []
        for jdata in jobs_data:
            job, _ = Job.objects.get_or_create(
                company=jdata['company'],
                title=jdata['title'],
                defaults=jdata
            )
            created_jobs.append(job)

        # 5. Sample Applications
        # Alice applies to Senior Python Engineer (Shortlisted)
        app1, _ = Application.objects.get_or_create(
            job=created_jobs[0],
            candidate=alice,
            defaults={
                'status': Application.Status.SHORTLISTED,
                'cover_letter': 'I have over 4 years of hands-on production experience architecting Django REST APIs and handling database migrations on PostgreSQL.',
                'recruiter_notes': 'Strong background and high skill match score. Scheduled for technical round.',
            }
        )
        if not app1.resume:
            app1.resume.save('alice_app1_resume.pdf', ContentFile(dummy_pdf))
            app1.save()

        # Alice applies to Backend Developer (Applied)
        app2, _ = Application.objects.get_or_create(
            job=created_jobs[1],
            candidate=alice,
            defaults={
                'status': Application.Status.APPLIED,
                'cover_letter': 'Excited by the asynchronous pipeline opportunities at Nexus. Looking forward to discussing.',
            }
        )
        if not app2.resume:
            app2.resume.save('alice_app2_resume.pdf', ContentFile(dummy_pdf))
            app2.save()

        # Bob applies to Full Stack Web Developer (Applied)
        app3, _ = Application.objects.get_or_create(
            job=created_jobs[2],
            candidate=bob,
            defaults={
                'status': Application.Status.APPLIED,
                'cover_letter': 'Passionate about combining Django REST Framework with interactive React frontends.',
            }
        )
        if not app3.resume:
            app3.resume.save('bob_app3_resume.pdf', ContentFile(dummy_pdf))
            app3.save()

        # Bob applies to FinTech Backend Architect (Rejected - experience mismatch)
        app4, _ = Application.objects.get_or_create(
            job=created_jobs[3],
            candidate=bob,
            defaults={
                'status': Application.Status.REJECTED,
                'cover_letter': 'Interested in moving into FinTech architecture.',
                'recruiter_notes': 'Candidate needs more years of experience for Architect-level seniority.',
            }
        )
        if not app4.resume:
            app4.resume.save('bob_app4_resume.pdf', ContentFile(dummy_pdf))
            app4.save()

        # 6. Sample Bookmarks / Saved Jobs
        SavedJob.objects.get_or_create(candidate=alice, job=created_jobs[3])
        SavedJob.objects.get_or_create(candidate=bob, job=created_jobs[5])

        self.stdout.write(self.style.SUCCESS("Demo database successfully seeded!"))
        self.stdout.write(self.style.SUCCESS("Admin: admin / admin123"))
        self.stdout.write(self.style.SUCCESS("Recruiter 1: sarah_recruiter / password123"))
        self.stdout.write(self.style.SUCCESS("Recruiter 2: vikram_recruiter / password123"))
        self.stdout.write(self.style.SUCCESS("Candidate 1: alice_dev / password123"))
        self.stdout.write(self.style.SUCCESS("Candidate 2: bob_coder / password123"))
