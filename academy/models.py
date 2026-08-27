"""
Database models for WIN PROFESSIONAL ACADEMY.
Includes Courses, Study Materials, Admission Guidance Streams, Results,
Inquiries, and Academy Branding Configuration.
"""
import os
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from .validators import (
    validate_document_file,
    validate_image_file,
    course_image_upload_path,
    course_material_upload_path,
    result_image_upload_path,
)


class AcademyProfile(models.Model):
    """
    Singleton configuration model storing editable academy metadata,
    official registration, taglines, phone numbers, and institution narrative.
    """
    academy_name = models.CharField(
        max_length=200,
        default="WIN PROFESSIONAL ACADEMY",
        help_text="Official institution name"
    )
    trust_name = models.CharField(
        max_length=200,
        default="Win Educational Trust",
        help_text="Trust running the academy"
    )
    trust_reg_no = models.CharField(
        max_length=100,
        default="379/2006",
        help_text="Official Trust Registration Number"
    )
    tagline = models.CharField(
        max_length=255,
        default="A Complete Guidelines for Higher Education & Job Service",
        help_text="Official Academy Tagline"
    )
    primary_phone = models.CharField(
        max_length=20,
        default="63817 06581",
        help_text="Primary contact phone number"
    )
    secondary_phone = models.CharField(
        max_length=20,
        default="86681 8494",
        help_text="Secondary contact phone number"
    )
    email = models.EmailField(
        default="info@winacademy.edu.in",
        blank=True,
        help_text="Official email address"
    )
    address = models.TextField(
        default="Tamil Nadu, India",
        help_text="Physical office / institution location"
    )
    whatsapp_number = models.CharField(
        max_length=20,
        default="6381706581",
        help_text="WhatsApp contact number without spaces"
    )
    mission = models.TextField(
        default="To empower every student with expert educational guidance, targeted competitive coaching, and comprehensive pathways towards prestigious universities and fulfilling careers.",
        help_text="Academy Mission statement"
    )
    vision = models.TextField(
        default="To stand as Tamil Nadu's premier educational lighthouse, unlocking global academic excellence and career success through dedicated mentorship and uncompromising standards.",
        help_text="Academy Vision statement"
    )
    higher_education_guidance = models.TextField(
        default="Comprehensive career mapping and admission assistance for Medical, Paramedical, Engineering, Agriculture, Law, and Arts & Science across Tamil Nadu, all-India institutions, and premier global universities.",
        help_text="Higher education guidance overview"
    )
    job_services_guidance = models.TextField(
        default="Dedicated coaching, mock interviews, syllabus mastery, and guidance for competitive teaching examinations (TRB, CSIR-NET, GATE) and governmental career placements.",
        help_text="Job guidance and services overview"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Academy Profile & Branding"
        verbose_name_plural = "Academy Profile & Branding"

    def __str__(self):
        return f"{self.academy_name} ({self.trust_name})"

    @classmethod
    def get_instance(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj


class CourseCategory(models.Model):
    """Categories for courses, allowing dynamic expansion by administrators."""
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    description = models.TextField(blank=True, help_text="Brief category description")
    display_order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Course Category"
        verbose_name_plural = "Course Categories"
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Course(models.Model):
    """
    Comprehensive course model supporting Mathematics coaching,
    guidance programs, syllabus breakdown, and dynamic file attachments.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        CourseCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses'
    )
    target_audience = models.CharField(
        max_length=200,
        blank=True,
        help_text="e.g. 'For College & University Students', 'Competitive Examination Coaching'"
    )
    short_description = models.TextField(
        help_text="Concise summary shown on course cards"
    )
    full_description = models.TextField(
        help_text="Detailed course description, curriculum overview, and methodology"
    )
    course_image = models.ImageField(
        upload_to=course_image_upload_path,
        validators=[validate_image_file],
        blank=True,
        null=True,
        help_text="High resolution course banner/card image"
    )
    syllabus = models.TextField(
        blank=True,
        help_text="Detailed syllabus or key topics (One per line or formatted text)"
    )
    duration = models.CharField(
        max_length=100,
        blank=True,
        default="Comprehensive Annual / Intensive Batch"
    )
    eligibility = models.CharField(
        max_length=200,
        blank=True,
        default="UG/PG Students & Aspirants"
    )
    batch_mode = models.CharField(
        max_length=100,
        blank=True,
        default="Classroom & Live Interactive Sessions"
    )
    is_featured = models.BooleanField(
        default=True,
        help_text="Show on homepage featured courses section"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether course is visible to public"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('academy:course_detail', kwargs={'slug': self.slug})

    @property
    def syllabus_list(self):
        """Returns list of topics split by newline."""
        if not self.syllabus:
            return []
        return [line.strip() for line in self.syllabus.splitlines() if line.strip()]


class CourseMaterial(models.Model):
    """
    Study materials, PDF notes, notebooks, and reference books
    attached to courses and stored securely in persistent storage.
    """
    MATERIAL_TYPES = (
        ('PDF', 'PDF Notes & Study Guides'),
        ('NOTE', 'Class Notebooks & Formulas'),
        ('BOOK', 'Reference Books & Compendiums'),
        ('SYLLABUS', 'Official Syllabus & Question Banks'),
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='materials'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    material_type = models.CharField(
        max_length=20,
        choices=MATERIAL_TYPES,
        default='PDF'
    )
    file = models.FileField(
        upload_to=course_material_upload_path,
        validators=[validate_document_file],
        help_text="Upload PDF, DOCX, or study documents (max 50MB)"
    )
    is_public = models.BooleanField(
        default=True,
        help_text="If True, accessible for public download"
    )
    display_order = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course Material"
        verbose_name_plural = "Course Materials"
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_material_type_display()})"

    @property
    def file_extension(self):
        if self.file and self.file.name:
            return os.path.splitext(self.file.name)[1].lower().replace('.', '').upper()
        return 'FILE'


class AdmissionGuidanceStream(models.Model):
    """
    Higher education streams guided by the academy:
    Medical, Paramedical, Engineering, Agriculture, Law, Arts & Science.
    """
    SCOPE_CHOICES = (
        ('TN', 'Tamil Nadu'),
        ('INDIA', 'All India (National)'),
        ('ABROAD', 'International & Abroad'),
        ('ALL', 'Tamil Nadu, India & Abroad'),
    )

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, default='ALL')
    icon_name = models.CharField(
        max_length=60,
        default="fas fa-graduation-cap",
        help_text="CSS icon class or descriptor (e.g. stethoscope, book, atom, tractor, balance-scale, flask)"
    )
    short_description = models.TextField(help_text="Brief highlight of colleges and counselling guidance")
    key_specializations = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated specializations (e.g., MBBS, BDS, Nursing, B.Tech, LLB)"
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Admission Guidance Stream"
        verbose_name_plural = "Admission Guidance Streams"
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_scope_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Result(models.Model):
    """Showcases student successes, competitive exam ranks, and selections."""
    student_name = models.CharField(max_length=150)
    examination = models.CharField(
        max_length=150,
        help_text="e.g. CSIR-NET JRF, GATE Mathematics, PG-TRB, IIT-JAM, University Topper"
    )
    year = models.CharField(max_length=20, default="2025-2026")
    score = models.CharField(max_length=50, blank=True, help_text="Marks / Percentile")
    rank = models.CharField(max_length=50, blank=True, help_text="e.g. AIR 14, State Rank 3")
    description = models.TextField(blank=True, help_text="Student's testimonial or success details")
    student_image = models.ImageField(
        upload_to=result_image_upload_path,
        validators=[validate_image_file],
        blank=True,
        null=True,
        help_text="Student photograph"
    )
    is_featured = models.BooleanField(default=True, help_text="Feature on homepage achievements showcase")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Student Result & Achievement"
        verbose_name_plural = "Student Results & Achievements"
        ordering = ['display_order', '-year', 'student_name']

    def __str__(self):
        return f"{self.student_name} - {self.examination} ({self.year})"


class ContactInquiry(models.Model):
    """Stores incoming inquiries from the Contact Us page into PostgreSQL."""
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=200, blank=True, default="General Inquiry")
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True, help_text="Internal notes by academy administrators")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry from {self.name} ({self.phone}) on {self.created_at.strftime('%Y-%m-%d')}"


class AdmissionInquiry(models.Model):
    """
    Stores structured admission and guidance applications submitted
    by students or parents across courses and streams.
    """
    STATUS_CHOICES = (
        ('PENDING', 'Pending Review'),
        ('CONTACTED', 'Counselor Contacted'),
        ('ADMITTED', 'Admission Confirmed'),
        ('CLOSED', 'Closed / Not Interested'),
    )

    student_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    interested_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admission_inquiries'
    )
    interested_stream = models.ForeignKey(
        AdmissionGuidanceStream,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admission_inquiries'
    )
    educational_qualification = models.CharField(
        max_length=200,
        blank=True,
        help_text="Current qualification (e.g. +2 / B.Sc Maths / B.E / M.Sc)"
    )
    message = models.TextField(blank=True, help_text="Specific requirements or queries")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    admin_notes = models.TextField(blank=True, help_text="Counseling status notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Admission & Guidance Application"
        verbose_name_plural = "Admission & Guidance Applications"
        ordering = ['-created_at']

    def __str__(self):
        course_str = self.interested_course.title if self.interested_course else "General Admission"
        return f"Application: {self.student_name} - {course_str} ({self.get_status_display()})"
