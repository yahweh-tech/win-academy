"""
Views for WIN PROFESSIONAL ACADEMY.
Handles public pages, form submissions into PostgreSQL, secure material downloads,
and operational health check endpoints.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, FileResponse, Http404, HttpResponseRedirect
from django.db.models import Q, F
from django.db import connection
from django.views.decorators.http import require_GET, require_http_methods
import os

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
from .forms import ContactForm, AdmissionApplicationForm


def get_client_ip(request):
    """Safely extracts client IP address accounting for proxies and reverse proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home_view(request):
    """
    Renders the rich homepage featuring Academy branding, Win Educational Trust details,
    Admission guidance streams (Medical, Paramedical, etc.), Mathematics courses,
    and achievements preview.
    """
    featured_courses = Course.objects.filter(is_active=True, is_featured=True).select_related('category').order_by('display_order')[:6]
    guidance_streams = AdmissionGuidanceStream.objects.filter(is_active=True).order_by('display_order')
    featured_results = Result.objects.filter(is_active=True, is_featured=True).order_by('display_order', '-year')[:6]
    
    # Quick admission modal form
    quick_admission_form = AdmissionApplicationForm()

    context = {
        'page_title': 'WIN PROFESSIONAL ACADEMY | Higher Education & Job Service',
        'featured_courses': featured_courses,
        'guidance_streams': guidance_streams,
        'featured_results': featured_results,
        'quick_admission_form': quick_admission_form,
    }
    return render(request, 'academy/home.html', context)


def courses_list_view(request):
    """
    Public course listing with search, category filtering, and responsive cards.
    """
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    courses = Course.objects.filter(is_active=True).select_related('category')

    if category_slug:
        courses = courses.filter(category__slug=category_slug)

    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(target_audience__icontains=query) |
            Q(syllabus__icontains=query)
        )

    categories = CourseCategory.objects.filter(is_active=True).order_by('display_order')

    context = {
        'page_title': 'Courses & Coaching Programs | WIN PROFESSIONAL ACADEMY',
        'courses': courses,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': query,
    }
    return render(request, 'academy/courses_list.html', context)


def course_detail_view(request, slug):
    """
    Detailed course page displaying syllabus breakdown, audience,
    downloadable public study materials, and direct application form.
    """
    course = get_object_or_404(Course.objects.select_related('category'), slug=slug, is_active=True)
    materials = course.materials.filter(is_public=True).order_by('display_order', '-created_at')
    other_courses = Course.objects.filter(is_active=True).exclude(id=course.id).order_by('display_order')[:4]
    
    # Pre-select this course in the application form
    application_form = AdmissionApplicationForm(initial={'interested_course': course})

    context = {
        'page_title': f'{course.title} | WIN PROFESSIONAL ACADEMY',
        'course': course,
        'materials': materials,
        'other_courses': other_courses,
        'application_form': application_form,
    }
    return render(request, 'academy/course_detail.html', context)


def about_view(request):
    """
    About Us page detailing Win Educational Trust (Reg. No. 379/2006),
    tagline, mission, vision, and comprehensive educational/job guidance services.
    """
    guidance_streams = AdmissionGuidanceStream.objects.filter(is_active=True).order_by('display_order')
    
    context = {
        'page_title': 'About Us | Win Educational Trust - WIN PROFESSIONAL ACADEMY',
        'guidance_streams': guidance_streams,
    }
    return render(request, 'academy/about.html', context)


def results_view(request):
    """
    Showcases student achievements, competitive examination ranks, and selections.
    """
    exam_filter = request.GET.get('exam', '').strip()
    results = Result.objects.filter(is_active=True)

    if exam_filter:
        results = results.filter(examination__icontains=exam_filter)

    results = results.order_by('display_order', '-year', 'student_name')
    
    # Get distinct examination names for quick filter pills
    available_exams = Result.objects.filter(is_active=True).values_list('examination', flat=True).distinct()

    context = {
        'page_title': 'Results & Achievements | WIN PROFESSIONAL ACADEMY',
        'results': results,
        'available_exams': sorted(set(available_exams)),
        'selected_exam': exam_filter,
    }
    return render(request, 'academy/results.html', context)


def contact_view(request):
    """
    Working Contact Us page. Validates user input and saves to PostgreSQL.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.ip_address = get_client_ip(request)
            inquiry.save()
            messages.success(
                request,
                f"Thank you, {inquiry.name}! Your enquiry has been received. Our team will contact you shortly at {inquiry.phone}."
            )
            return redirect('academy:contact')
        else:
            messages.error(request, "Please correct the highlighted errors in the contact form.")
    else:
        form = ContactForm()

    context = {
        'page_title': 'Contact Us | WIN PROFESSIONAL ACADEMY',
        'form': form,
    }
    return render(request, 'academy/contact.html', context)


def admissions_view(request):
    """
    Dedicated Admissions & Counseling Application page.
    Saves applications to PostgreSQL for the administrator.
    """
    initial_data = {}
    course_slug = request.GET.get('course', '').strip()
    if course_slug:
        course = Course.objects.filter(slug=course_slug, is_active=True).first()
        if course:
            initial_data['interested_course'] = course

    if request.method == 'POST':
        form = AdmissionApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            course_title = application.interested_course.title if application.interested_course else "Academic Guidance"
            messages.success(
                request,
                f"Application Submitted! Thank you {application.student_name}. Your application for '{course_title}' has been registered. Our counselors will call you on {application.phone}."
            )
            return redirect('academy:admissions')
        else:
            messages.error(request, "Please check the form and fill in all required fields.")
    else:
        form = AdmissionApplicationForm(initial=initial_data)

    context = {
        'page_title': 'Admissions Open | Apply Now - WIN PROFESSIONAL ACADEMY',
        'form': form,
    }
    return render(request, 'academy/admissions.html', context)


def download_material_view(request, pk):
    """
    Secure download handler for course study materials.
    Tracks download counts and serves files safely.
    """
    material = get_object_or_404(CourseMaterial, pk=pk, is_public=True)
    
    # Increment download count using atomic F expression
    CourseMaterial.objects.filter(pk=pk).update(download_count=F('download_count') + 1)
    
    if not material.file:
        raise Http404("Requested file does not exist.")

    # Redirect to S3 storage URL if cloud storage is active, or serve FileResponse locally
    try:
        url = material.file.url
        return HttpResponseRedirect(url)
    except Exception:
        # Fallback to direct file response for local filesystem
        try:
            return FileResponse(material.file.open('rb'), as_attachment=True, filename=os.path.basename(material.file.name))
        except Exception:
            raise Http404("Error retrieving file.")


@require_GET
def health_check_view(request):
    """
    Operational Health Check endpoint for Render, Docker, and uptime monitors.
    Validates database connectivity and returns JSON.
    """
    db_status = "ok"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as e:
        db_status = f"database error: {str(e)}"
        return JsonResponse({
            "status": "unhealthy",
            "database": db_status,
            "academy": "WIN PROFESSIONAL ACADEMY",
        }, status=503)

    return JsonResponse({
        "status": "ok",
        "database": "connected",
        "academy": "WIN PROFESSIONAL ACADEMY",
        "trust": "Win Educational Trust (Reg. No. 379/2006)",
        "tagline": "A Complete Guidelines for Higher Education & Job Service",
    }, status=200)


def custom_404_view(request, exception=None):
    """Custom branded 404 page."""
    return render(request, '404.html', status=404)


def custom_500_view(request):
    """Custom branded 500 page."""
    return render(request, '500.html', status=500)
