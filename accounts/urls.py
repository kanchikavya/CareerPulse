from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/candidate/', views.register_candidate, name='register_candidate'),
    path('register/recruiter/', views.register_recruiter, name='register_recruiter'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/candidate/', views.candidate_profile, name='candidate_profile'),
    path('profile/company/', views.company_profile, name='company_profile'),
]
