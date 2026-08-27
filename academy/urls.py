"""
URL configuration for the academy app.
"""
from django.urls import path
from . import views

app_name = 'academy'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('courses/', views.courses_list_view, name='courses'),
    path('courses/<slug:slug>/', views.course_detail_view, name='course_detail'),
    path('about/', views.about_view, name='about'),
    path('results/', views.results_view, name='results'),
    path('contact/', views.contact_view, name='contact'),
    path('admissions/', views.admissions_view, name='admissions'),
    path('apply/', views.admissions_view, name='apply'),  # Clean alias
    path('materials/<int:pk>/download/', views.download_material_view, name='download_material'),
    path('health/', views.health_check_view, name='health'),
]
