"""
Comprehensive test suite for WIN PROFESSIONAL ACADEMY platform.
Tests models, views, forms, health check, file upload validators, and database storage.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

from .models import (
    AcademyProfile,
    CourseCategory,
    Course,
    CourseMaterial,
    AdmissionGuidanceStream,
    Result,
    ContactInquiry,
    AdmissionInquiry,
)
from .validators import validate_document_file, validate_image_file


class AcademySystemTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Seed profile
        self.profile = AcademyProfile.objects.create(
            academy_name="WIN PROFESSIONAL ACADEMY",
            trust_name="Win Educational Trust",
            trust_reg_no="379/2006",
            tagline="A Complete Guidelines for Higher Education & Job Service",
            primary_phone="63817 06581",
            secondary_phone="86681 8494",
        )

        # Seed category
        self.category = CourseCategory.objects.create(
            name="Mathematics Coaching",
            slug="mathematics-coaching",
            display_order=1,
            is_active=True,
        )

        # Seed course
        self.course = Course.objects.create(
            title="Engineering Mathematics",
            slug="engineering-mathematics",
            category=self.category,
            target_audience="For College & University Students",
            short_description="Coaching for Engineering Mathematics.",
            full_description="Detailed curriculum covering calculus and linear algebra.",
            syllabus="Matrices\nCalculus\nDifferential Equations",
            is_featured=True,
            is_active=True,
        )

        # Seed stream
        self.stream = AdmissionGuidanceStream.objects.create(
            name="Medical",
            slug="medical",
            scope="ALL",
            short_description="MBBS and BDS guidance.",
            is_active=True,
        )

        # Seed result
        self.result = Result.objects.create(
            student_name="Test Student",
            examination="CSIR-NET Mathematical Sciences",
            rank="AIR 1",
            year="2025-2026",
            is_active=True,
            is_featured=True,
        )

    def test_health_check_endpoint(self):
        """Verify that /health/ returns 200 and healthy JSON response."""
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'ok')
        self.assertEqual(data.get('database'), 'connected')
        self.assertEqual(data.get('academy'), 'WIN PROFESSIONAL ACADEMY')

    def test_homepage_view(self):
        """Verify homepage loads with branding, trust info, and phone numbers."""
        response = self.client.get(reverse('academy:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "WIN PROFESSIONAL ACADEMY")
        self.assertContains(response, "379/2006")
        self.assertContains(response, "63817 06581")
        self.assertContains(response, "86681 8494")
        self.assertContains(response, "Engineering Mathematics")

    def test_courses_listing_view(self):
        """Verify courses listing page and search filter."""
        response = self.client.get(reverse('academy:courses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Engineering Mathematics")

        # Search test
        response_search = self.client.get(reverse('academy:courses') + '?q=Engineering')
        self.assertEqual(response_search.status_code, 200)
        self.assertContains(response_search, "Engineering Mathematics")

        # Non-matching search
        response_empty = self.client.get(reverse('academy:courses') + '?q=NonExistentCourseXYZ')
        self.assertEqual(response_empty.status_code, 200)
        self.assertContains(response_empty, "No courses matched your query")

    def test_course_detail_view(self):
        """Verify individual course page and 404 for nonexistent course."""
        response = self.client.get(reverse('academy:course_detail', kwargs={'slug': 'engineering-mathematics'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Engineering Mathematics")
        self.assertContains(response, "Matrices")

        # 404 test
        response_404 = self.client.get(reverse('academy:course_detail', kwargs={'slug': 'non-existent'}))
        self.assertEqual(response_404.status_code, 404)

    def test_about_us_view(self):
        """Verify About Us page renders trust details and mission/vision."""
        response = self.client.get(reverse('academy:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Win Educational Trust")
        self.assertContains(response, "379/2006")

    def test_results_view(self):
        """Verify public results and achievements page."""
        response = self.client.get(reverse('academy:results'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Student")
        self.assertContains(response, "AIR 1")

    def test_contact_form_submission(self):
        """Verify contact form validates and persists inquiry in the database."""
        post_data = {
            'name': 'Ramesh Kumar',
            'phone': '9876543210',
            'email': 'ramesh@example.com',
            'subject': 'Admission Query for TRB Maths',
            'message': 'Please share batch timings and fees for upcoming TRB batches.',
        }
        response = self.client.post(reverse('academy:contact'), data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactInquiry.objects.filter(phone='9876543210').exists())
        inquiry = ContactInquiry.objects.get(phone='9876543210')
        self.assertEqual(inquiry.name, 'Ramesh Kumar')
        self.assertEqual(inquiry.subject, 'Admission Query for TRB Maths')

    def test_admissions_form_submission(self):
        """Verify admission application form validates and persists in database."""
        post_data = {
            'student_name': 'Sangeetha M',
            'phone': '9123456780',
            'email': 'sangeetha@example.com',
            'interested_course': self.course.id,
            'interested_stream': self.stream.id,
            'educational_qualification': 'B.Sc Mathematics Final Year',
            'message': 'Interested in joining weekend batches.',
        }
        response = self.client.post(reverse('academy:admissions'), data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(AdmissionInquiry.objects.filter(phone='9123456780').exists())
        application = AdmissionInquiry.objects.get(phone='9123456780')
        self.assertEqual(application.student_name, 'Sangeetha M')
        self.assertEqual(application.interested_course, self.course)
        self.assertEqual(application.status, 'PENDING')

    def test_file_validators(self):
        """Verify upload security validators for allowed extensions and sizes."""
        # Valid PDF file
        valid_pdf = SimpleUploadedFile("sample.pdf", b"%PDF-1.4 test document content", content_type="application/pdf")
        validate_document_file(valid_pdf)  # Should not raise

        # Invalid executable / script file
        invalid_file = SimpleUploadedFile("malicious.exe", b"binary content", content_type="application/x-msdownload")
        with self.assertRaises(ValidationError):
            validate_document_file(invalid_file)

        # Valid Image file
        valid_img = SimpleUploadedFile("photo.jpg", b"image data", content_type="image/jpeg")
        validate_image_file(valid_img)  # Should not raise
