"""
Forms for WIN PROFESSIONAL ACADEMY.
Provides validated user input processing for Contact Enquiries and Admission Applications.
"""
from django import forms
from .models import ContactInquiry, AdmissionInquiry, Course, AdmissionGuidanceStream


class ContactForm(forms.ModelForm):
    """Clean, validated form for user enquiries from the Contact page."""
    # Simple honeypot to prevent automated bot spam
    website_hp = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactInquiry
        fields = ['name', 'phone', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name *',
                'required': True,
                'id': 'contact_name',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile Phone Number *',
                'required': True,
                'id': 'contact_phone',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address (Optional)',
                'id': 'contact_email',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject / Topic *',
                'required': True,
                'id': 'contact_subject',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'How can we help you? *',
                'required': True,
                'id': 'contact_message',
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        # Ensure digits presence
        digits = [c for c in phone if c.isdigit()]
        if len(digits) < 7:
            raise forms.ValidationError("Please provide a valid contact number (at least 7 digits).")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        hp = cleaned_data.get('website_hp')
        if hp:
            # Bot trap triggered
            raise forms.ValidationError("Spam submission detected.")
        return cleaned_data


class AdmissionApplicationForm(forms.ModelForm):
    """Validated admission and educational counseling application form."""
    website_hp = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = AdmissionInquiry
        fields = [
            'student_name',
            'phone',
            'email',
            'interested_course',
            'interested_stream',
            'educational_qualification',
            'message',
        ]
        widgets = {
            'student_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Student Full Name *',
                'required': True,
                'id': 'admission_name',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Primary Phone / WhatsApp *',
                'required': True,
                'id': 'admission_phone',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address (Optional)',
                'id': 'admission_email',
            }),
            'interested_course': forms.Select(attrs={
                'class': 'form-select',
                'id': 'admission_course',
            }),
            'interested_stream': forms.Select(attrs={
                'class': 'form-select',
                'id': 'admission_stream',
            }),
            'educational_qualification': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Current Qualification (e.g. +2, B.Sc Maths, B.E) *',
                'required': True,
                'id': 'admission_qualification',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any specific query or target entrance exam?',
                'id': 'admission_message',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['interested_course'].queryset = Course.objects.filter(is_active=True).order_by('display_order', 'title')
        self.fields['interested_course'].empty_label = "-- Select Course (Optional) --"
        self.fields['interested_stream'].queryset = AdmissionGuidanceStream.objects.filter(is_active=True).order_by('display_order')
        self.fields['interested_stream'].empty_label = "-- Select Guidance Stream (Optional) --"

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        digits = [c for c in phone if c.isdigit()]
        if len(digits) < 7:
            raise forms.ValidationError("Please provide a valid phone number (at least 7 digits).")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        hp = cleaned_data.get('website_hp')
        if hp:
            raise forms.ValidationError("Spam submission detected.")
        return cleaned_data
