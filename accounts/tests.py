from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import User, CandidateProfile, Company
from accounts.validators import validate_pdf_extension, validate_file_size


class AccountModelTests(TestCase):
    def setUp(self):
        self.candidate_user = User.objects.create_user(
            username='test_candidate',
            email='candidate@test.com',
            password='password123',
            role=User.Role.CANDIDATE
        )
        self.recruiter_user = User.objects.create_user(
            username='test_recruiter',
            email='recruiter@test.com',
            password='password123',
            role=User.Role.RECRUITER
        )

    def test_user_roles(self):
        self.assertTrue(self.candidate_user.is_candidate)
        self.assertFalse(self.candidate_user.is_recruiter)

        self.assertTrue(self.recruiter_user.is_recruiter)
        self.assertFalse(self.recruiter_user.is_candidate)

    def test_candidate_profile_skills_parsing(self):
        profile = CandidateProfile.objects.create(
            user=self.candidate_user,
            skills="Python, Django, PostgreSQL, Docker"
        )
        skills = profile.get_skills_list()
        self.assertEqual(len(skills), 4)
        self.assertIn("python", skills)
        self.assertIn("postgresql", skills)

    def test_pdf_validator_accepts_pdf(self):
        valid_file = SimpleUploadedFile("resume.pdf", b"%PDF-1.4 sample content", content_type="application/pdf")
        try:
            validate_pdf_extension(valid_file)
        except ValidationError:
            self.fail("validate_pdf_extension raised ValidationError unexpectedly on valid pdf!")

    def test_pdf_validator_rejects_non_pdf(self):
        invalid_file = SimpleUploadedFile("resume.docx", b"word doc content", content_type="application/msword")
        with self.assertRaises(ValidationError):
            validate_pdf_extension(invalid_file)
