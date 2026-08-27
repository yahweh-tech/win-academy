"""
Context processors to supply academy profile, contact numbers, trust details,
and active courses globally across all templates.
"""
from .models import AcademyProfile, Course, CourseCategory


def academy_context(request):
    """Injects academy branding, contact details, and top courses to templates."""
    profile = AcademyProfile.get_instance()
    header_courses = Course.objects.filter(is_active=True).order_by('display_order', 'title')[:6]
    categories = CourseCategory.objects.filter(is_active=True).order_by('display_order')

    return {
        'academy_profile': profile,
        'academy_name': profile.academy_name,
        'trust_name': profile.trust_name,
        'trust_reg_no': profile.trust_reg_no,
        'tagline': profile.tagline,
        'primary_phone': profile.primary_phone,
        'secondary_phone': profile.secondary_phone,
        'header_courses': header_courses,
        'nav_categories': categories,
    }
