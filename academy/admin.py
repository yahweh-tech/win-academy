"""
Django Admin customization for WIN PROFESSIONAL ACADEMY.
Provides an easy-to-use control panel for academy owners to manage courses,
materials, inquiries, admission applications, results, and academy metadata.
"""
from django.contrib import admin
from django.utils.html import format_html
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


@admin.register(AcademyProfile)
class AcademyProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Academy & Trust Identity", {
            'fields': ('academy_name', 'trust_name', 'trust_reg_no', 'tagline'),
            'description': 'Core branding and legal registration details.'
        }),
        ("Official Contacts & Location", {
            'fields': ('primary_phone', 'secondary_phone', 'whatsapp_number', 'email', 'address'),
            'description': 'Direct hotline numbers shown in the website header and contact bar.'
        }),
        ("Institutional Narrative & Guidance Services", {
            'fields': ('mission', 'vision', 'higher_education_guidance', 'job_services_guidance'),
            'description': 'Editable sections displayed on the About Us and Guidance pages.'
        }),
    )

    def has_add_permission(self, request):
        # Prevent creating multiple profiles (singleton)
        return not AcademyProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class CourseMaterialInline(admin.TabularInline):
    model = CourseMaterial
    extra = 1
    fields = ('title', 'material_type', 'file', 'is_public', 'display_order')
    classes = ('collapse',)


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_order', 'is_active', 'created_at')
    list_editable = ('display_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'target_audience', 'is_featured', 'is_active', 'display_order', 'created_at')
    list_filter = ('category', 'is_active', 'is_featured')
    list_editable = ('is_featured', 'is_active', 'display_order')
    search_fields = ('title', 'short_description', 'full_description', 'target_audience')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CourseMaterialInline]
    fieldsets = (
        ("Basic Information", {
            'fields': ('title', 'slug', 'category', 'target_audience', 'course_image')
        }),
        ("Descriptions & Curriculum", {
            'fields': ('short_description', 'full_description', 'syllabus')
        }),
        ("Batch Details", {
            'fields': ('duration', 'eligibility', 'batch_mode')
        }),
        ("Publishing & Display", {
            'fields': ('is_featured', 'is_active', 'display_order')
        }),
    )


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'material_type', 'is_public', 'download_count', 'display_order', 'created_at')
    list_filter = ('material_type', 'is_public', 'course')
    list_editable = ('is_public', 'display_order')
    search_fields = ('title', 'description', 'course__title')


@admin.register(AdmissionGuidanceStream)
class AdmissionGuidanceStreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'scope', 'key_specializations', 'is_active', 'display_order')
    list_editable = ('is_active', 'display_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'short_description', 'key_specializations')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'examination', 'year', 'rank', 'score', 'is_featured', 'is_active', 'display_order')
    list_filter = ('examination', 'year', 'is_featured', 'is_active')
    list_editable = ('is_featured', 'is_active', 'display_order')
    search_fields = ('student_name', 'examination', 'rank', 'score', 'description')


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'subject', 'is_resolved_badge', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('name', 'phone', 'email', 'subject', 'message')
    readonly_fields = ('name', 'phone', 'email', 'subject', 'message', 'ip_address', 'created_at')
    actions = ['mark_as_resolved', 'mark_as_unresolved']

    def is_resolved_badge(self, obj):
        if obj.is_resolved:
            return format_html('<span style="color: #10B981; font-weight: bold;">✔ Resolved</span>')
        return format_html('<span style="color: #EF4444; font-weight: bold;">⏳ Pending</span>')
    is_resolved_badge.short_description = 'Status'

    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
    mark_as_resolved.short_description = "Mark selected inquiries as Resolved"

    def mark_as_unresolved(self, request, queryset):
        queryset.update(is_resolved=False)
    mark_as_unresolved.short_description = "Mark selected inquiries as Pending"


@admin.register(AdmissionInquiry)
class AdmissionInquiryAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'phone', 'interested_course', 'status_badge', 'educational_qualification', 'created_at')
    list_filter = ('status', 'interested_course', 'interested_stream', 'created_at')
    search_fields = ('student_name', 'phone', 'email', 'educational_qualification', 'message')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_contacted', 'mark_as_admitted']

    def status_badge(self, obj):
        colors = {
            'PENDING': '#F59E0B',
            'CONTACTED': '#3B82F6',
            'ADMITTED': '#10B981',
            'CLOSED': '#6B7280',
        }
        color = colors.get(obj.status, '#6B7280')
        return format_html(
            '<span style="background-color: {}; color: #fff; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Application Status'

    def mark_as_contacted(self, request, queryset):
        queryset.update(status='CONTACTED')
    mark_as_contacted.short_description = "Mark as Counselor Contacted"

    def mark_as_admitted(self, request, queryset):
        queryset.update(status='ADMITTED')
    mark_as_admitted.short_description = "Mark as Admission Confirmed"
