"""
File validation and security utilities for WIN PROFESSIONAL ACADEMY.
Ensures uploaded study materials, notes, books, and images adhere to safety standards.
"""
import os
import uuid
from django.core.exceptions import ValidationError
from django.utils.text import slugify


MAX_DOCUMENT_SIZE_MB = 50
MAX_IMAGE_SIZE_MB = 10
ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx', '.epub', '.zip']
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']


def validate_document_file(file):
    """Validate document extension and file size."""
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file extension '{ext}'. Allowed extensions: {', '.join(ALLOWED_DOCUMENT_EXTENSIONS)}"
        )
    
    file_size_mb = file.size / (1024 * 1024)
    if file_size_mb > MAX_DOCUMENT_SIZE_MB:
        raise ValidationError(
            f"File size ({file_size_mb:.1f} MB) exceeds maximum allowed size of {MAX_DOCUMENT_SIZE_MB} MB."
        )


def validate_image_file(file):
    """Validate image extension and file size."""
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f"Unsupported image extension '{ext}'. Allowed extensions: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        )
    
    file_size_mb = file.size / (1024 * 1024)
    if file_size_mb > MAX_IMAGE_SIZE_MB:
        raise ValidationError(
            f"Image size ({file_size_mb:.1f} MB) exceeds maximum allowed size of {MAX_IMAGE_SIZE_MB} MB."
        )


def generate_secure_upload_path(instance, filename, folder_prefix="materials"):
    """
    Generates a secure, sanitized unique path to prevent path traversal and collisions.
    Example: materials/course-slug/2026/08/unique_id_clean_filename.pdf
    """
    ext = os.path.splitext(filename)[1].lower()
    base_name = os.path.splitext(filename)[0]
    safe_name = slugify(base_name)[:40] or "file"
    unique_id = uuid.uuid4().hex[:10]
    
    course_slug = "general"
    if hasattr(instance, 'course') and instance.course:
        course_slug = instance.course.slug
    elif hasattr(instance, 'slug') and instance.slug:
        course_slug = instance.slug

    return f"{folder_prefix}/{course_slug}/{unique_id}_{safe_name}{ext}"


def course_image_upload_path(instance, filename):
    return generate_secure_upload_path(instance, filename, folder_prefix="courses")


def course_material_upload_path(instance, filename):
    return generate_secure_upload_path(instance, filename, folder_prefix="materials")


def result_image_upload_path(instance, filename):
    return generate_secure_upload_path(instance, filename, folder_prefix="results")
