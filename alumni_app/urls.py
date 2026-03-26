from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    # --- 1. AUTHENTICATION & REGISTRATION ---
    
    # Sign Up: Creates User + Links to SQL Server Record
    path('auth/register/', views.register_alumni, name='register-alumni'),
    
    # Login: Send username/password to get Access + Refresh tokens
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Refresh: Get a new Access token using a Refresh token
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # --- 2. ALUMNI DIRECTORY (Verified Only) ---
    path('alumni/', views.AlumniList.as_view(), name='alumni-list'),
    path('alumni/<int:pk>/', views.AlumniDetail.as_view(), name='alumni-detail'),


    # --- 3. PUBLIC STATISTICS (Anyone) ---
    path('stats/donors/', views.donor_statistics, name='donor-stats'),
    path('stats/events/', views.event_popularity, name='event-stats'),


    # --- 4. UNIVERSITY OFFERINGS (Public) ---
    path('events/', views.EventList.as_view(), name='event-list'),
    path('programs/', views.ProgramList.as_view(), name='program-list'),


    # --- 5. TRANSACTIONS & AWARDS (Logged-in) ---
    path('awards/', views.AwardList.as_view(), name='award-list'),
    path('donations/', views.DonationList.as_view(), name='donation-list'),
]