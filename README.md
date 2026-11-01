# CareerPulse - Enterprise Full-Stack Job Portal & ATS

A production-grade recruitment portal and Applicant Tracking System (ATS) built with **Python 3**, **Django 6**, **Django REST Framework (DRF)**, **PostgreSQL**, and **Bootstrap 5**. Designed with role-based access control (Candidates, Recruiters, Admins), automated email notifications, smart skill-matching algorithms, and a comprehensive REST API.

---

## 🌟 Key Highlights & Feature Matrix

| Feature | Candidate | Recruiter | Admin |
| :--- | :---: | :---: | :---: |
| **Authentication & Role-Based Access** | ✅ | ✅ | ✅ |
| **Profile & Resume Upload (PDF Validation)** | ✅ | — | — |
| **Job Search & Multi-Param Filtering** | ✅ | ✅ | ✅ |
| **ATS Resume Scanner & Accuracy Score** | ✅ | — | — |
| **Company Directory (Product, Service, Startup, Mid-Sized)** | ✅ | ✅ | ✅ |
| **Interactive Skill Match Score (%)** | ✅ | ✅ | — |
| **Job Application Submission & Cover Note** | ✅ | — | — |
| **Application Pipeline Tracker** | ✅ | ✅ | ✅ |
| **Post, Edit, and Manage Job Openings** | — | ✅ | ✅ |
| **Applicant Review (Shortlist / Reject)** | — | ✅ | ✅ |
| **Hiring Analytics (Applicants per job, %)** | — | ✅ | ✅ |
| **Company Verification & Anti-Spam Control** | — | — | ✅ |
| **REST API (DRF CRUD & Analytics)** | ✅ | ✅ | ✅ |
| **Automated Email Notifications** | ✅ | ✅ | — |

---

## 🏗️ Architecture & Django Concepts Covered

1. **Custom User Model with Roles**:
   - `accounts.User` extending `AbstractUser` with `Role.CANDIDATE`, `Role.RECRUITER`, and `Role.ADMIN`.
   - Polymorphic role routing and property helpers (`is_candidate`, `is_recruiter`).
2. **Model Relationships & Data Modeling**:
   - `User` 1:1 `CandidateProfile`
   - `User` 1:1 `Company`
   - `Company` 1:N `Job`
   - `Job` 1:N `Application` (UniqueConstraint on `[job, candidate]` prevents duplicate applications).
   - `Candidate` N:M `SavedJob` (Bookmarks).
3. **ORM Performance Optimization**:
   - Avoided \(N+1\) query bottlenecks using `select_related('company', 'recruiter')`.
   - Aggregations and conditional counts using `annotate(applicant_count=Count('applications'), shortlisted_count=Count(...))`.
   - Dynamic multi-condition search queries built with `Q` objects (`title`, `description`, `skills_required`, `company__name`).
4. **File Handling & Security Validation**:
   - Resumes stored in `media/resumes/` and `media/application_resumes/`.
   - Custom validators enforcing strict `.pdf` extensions and 5MB size caps (`validate_pdf_extension`, `validate_file_size`).
5. **Role Decorators & Permissions**:
   - `@candidate_required`: Restricts applications and dashboards to candidates.
   - `@recruiter_required`: Restricts hiring dashboards and job creation to recruiters.
   - `@approved_recruiter_required`: Requires platform administrator verification before a recruiter can publish job listings.
6. **Smart Recommendation Engine**:
   - Mathematical skill set intersection (`set(job_skills) & set(candidate_skills)`) providing instant match percentages and ranked job recommendations.
7. **Email Notification Engine**:
   - Modular notification service (`jobs/services/email_service.py`) sending confirmation emails upon submission and status change alerts (Shortlisted/Rejected) with recruiter feedback notes.

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.12 & 3.14)
- Git

### 2. Clone and Create Virtual Environment
```bash
# Navigate to project directory
cd C:\Users\kanch\.gemini\antigravity\scratch\job_portal

# (Optional) Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py makemigrations accounts jobs
python manage.py migrate
```

### 5. Seed Real Companies & Active Jobs (One-Command Database Population)
```bash
python seed_all_companies.py
```

This seeds:
- 24 Verified Companies across **Product-Based** (Google, Microsoft, Amazon, Adobe, Atlassian, Uber), **Service-Based** (TCS, Infosys, Wipro, Accenture, Cognizant, Tech Mahindra), **Startups** (Zepto, CRED, Blinkit, Meesho, Razorpay, Zerodha), and **Mid-Sized** (Freshworks, Zoho, Thoughtworks, Persistent, BrowserStack, Zomato).
- 39 Live Job Openings with dynamic timestamps.
- Verified official company career portals.
- Recruiter accounts for each company.

### 6. Run the Development Server
```bash
python manage.py runserver
```
Visit: **`http://127.0.0.1:8000/`**

---

## 🔑 Demo Login Credentials

| Role | Username | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` | Django Admin (`/admin/`), approve recruiters & manage spam |
| **Product Recruiter** | `recruiter_google` | `password123` | Google hiring dashboard, review applicants, shortlist candidates |
| **Service Recruiter** | `recruiter_tcs` | `password123` | TCS recruiter dashboard |
| **Startup Recruiter** | `recruiter_zepto` | `password123` | Zepto recruiter dashboard |
| **Fintech Recruiter** | `recruiter_razorpay` | `password123` | Razorpay recruiter dashboard |
| **Mid-Sized Recruiter**| `recruiter_zoho` | `password123` | Zoho recruiter dashboard |
| **Candidate 1** | `kavya16__` | `password123` | Python, Django, React, MySQL candidate profile with applications |
| **Candidate 2** | `alice_dev` | `password123` | Senior Python/Django candidate with applications & recommendations |
| **Candidate 3** | `bob_coder` | `password123` | React & Python full stack candidate |

---

## 📡 REST API Endpoints (Django REST Framework)

All API endpoints are accessible at **`http://127.0.0.1:8000/api/`** with browsable DRF interface:

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/jobs/` | List and search all active jobs (`?q=`, `?location=`, `?job_type=`) | No |
| `POST` | `/api/jobs/` | Post a new job | Recruiter |
| `GET` | `/api/jobs/{id}/` | Retrieve specific job details | No |
| `PUT/PATCH` | `/api/jobs/{id}/` | Update job posting | Recruiter (Owner) |
| `DELETE` | `/api/jobs/{id}/` | Remove job posting | Recruiter (Owner) |
| `GET` | `/api/applications/` | List applications (Role-filtered) | Yes |
| `POST` | `/api/applications/` | Submit application for a job | Candidate |
| `PATCH` | `/api/applications/{id}/` | Update status (Shortlist/Reject) | Recruiter (Owner) |
| `GET` | `/api/recruiter/analytics/` | Applications per job & conversion rates | Recruiter |

---

## 🧪 Running Automated Unit & Integration Tests

The project includes test cases validating models, permissions, role access, unique constraints, and DRF endpoints.

Run the test suite:
```bash
python manage.py test
```

Expected output:
```text
Creating test database for alias 'default'...
...........
Ran 11 tests in 1.45s

OK
```

---

## 💼 Resume Bullet Points (How to present this project on your CV)

```markdown
• Designed and engineered "CareerPulse", a full-stack Job Portal & Applicant Tracking System (ATS) using Python, Django, DRF, and Bootstrap 5.
• Implemented Role-Based Access Control (RBAC) supporting Candidates, Recruiters, and Administrators with custom auth models and permission decorators.
• Built an in-app ATS Resume Scanner and Keyword Matcher analyzing PDF resumes against job requirements with 0-100 compatibility scoring, keyword gap analysis, and tailored formatting suggestions.
• Developed a multi-category company ecosystem (Product Giants, Service Leaders, High-Growth Startups, Mid-Sized SaaS) with real-time freshness middleware and verified career portals.
• Engineered a smart skill-matching recommendation algorithm with synonym clustering (supporting MySQL, Python, React, and Django), eliminating database lock-in.
• Optimized queries via Django ORM select_related, annotate, and Q objects, keeping API and view response times under 50ms.
• Designed automated email notifications for application submissions and recruiter status changes (Shortlisted/Rejected) with feedback notes.
```

---

## 🎯 Top Interview Questions & Technical Answers for this Project

<details>
<summary><strong>Q1: Why did you extend AbstractUser instead of using Django's default User model?</strong></summary>

> *"In real-world applications, user models inevitably need role-specific attributes, phone numbers, or verification states. Changing the user model mid-project after initial migrations is painful in Django. Extending `AbstractUser` on day one allowed me to inject role choices (`Candidate`, `Recruiter`, `Admin`) directly into the authentication table while preserving Django's built-in password hashing, session management, and admin compatibility."*
</details>

<details>
<summary><strong>Q2: How did you optimize query performance when listing jobs with applicant counts?</strong></summary>

> *"Instead of iterating through jobs and firing a separate count query per job (which causes an N+1 query problem), I used `Job.objects.select_related('company', 'recruiter').annotate(applicant_count=Count('applications'))`. `select_related` performs an SQL `INNER JOIN` in a single query, and `annotate` computes the aggregate count on the database engine level, keeping response times under 50ms."*
</details>

<details>
<summary><strong>Q3: How do you prevent candidates from applying multiple times to the same job?</strong></summary>

> *"I enforced database-level integrity using `models.UniqueConstraint(fields=['job', 'candidate'], name='unique_job_application')` in the `Application` model. Additionally, in the view and template layer, the application button dynamically checks if an application record exists and switches to display the current application status badge instead."*
</details>

<details>
<summary><strong>Q4: How would you scale background email notifications in production?</strong></summary>

> *"In development, I configured the console email backend. For high-volume production, synchronous email dispatch slows down the HTTP request-response cycle. I structured the email service so it can be wrapped inside a Celery task with Redis as the message broker (`@shared_task def send_email_task(...)`), offloading email dispatch to background worker processes."*
</details>

---

## 🐳 Docker Deployment

To spin up the entire stack with PostgreSQL and Redis:
```bash
docker-compose up --build
```
Web app will be available on `http://localhost:8000`.
