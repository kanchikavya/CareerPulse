from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('jobs/', views.job_list_view, name='job_list'),
    path('companies/', views.company_list_view, name='company_list'),
    path('companies/<int:pk>/', views.company_detail_view, name='company_detail'),
    path('ats-checker/', views.ats_checker_view, name='ats_checker'),
    path('jobs/<int:job_id>/ats-checker/', views.ats_checker_view, name='ats_checker_with_job'),
    path('jobs/post/', views.job_create_view, name='job_create'),
    path('jobs/<int:pk>/', views.job_detail_view, name='job_detail'),
    path('jobs/<int:pk>/edit/', views.job_update_view, name='job_update'),
    path('jobs/<int:pk>/delete/', views.job_delete_view, name='job_delete'),
    path('jobs/<int:pk>/apply/', views.apply_job_view, name='apply_job'),
    path('jobs/<int:pk>/save/', views.toggle_save_job, name='toggle_save_job'),

    # Dashboards
    path('dashboard/candidate/', views.candidate_dashboard_view, name='candidate_dashboard'),
    path('dashboard/recruiter/', views.recruiter_dashboard_view, name='recruiter_dashboard'),
    path('dashboard/recruiter/job/<int:pk>/applicants/', views.recruiter_job_applicants_view, name='recruiter_applicants'),
]
