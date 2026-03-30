from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # --- 1. AUTHENTICATION & REGISTRATION ---
    path('auth/register/', views.register_alumni, name='register-alumni'),
    path('auth/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # --- 2. ALUMNI DIRECTORY ---
    path('alumni/', views.AlumniList.as_view(), name='alumni-list'),
    path('alumni/<int:pk>/', views.AlumniDetail.as_view(), name='alumni-detail'),


    # --- 3. ADMIN MANAGEMENT (Core Dashboard) ---
    path('admin/alumni/', views.AdminAlumniList.as_view(), name='admin-alumni-list'),
    path('admin/verify/<int:pk>/', views.verify_alumnus_manual, name='admin-verify-alumnus'),


    # --- 4. PARTNERSHIP & EXTERNAL RELATIONS ---
    path('admin/institutions/', views.InstitutionList.as_view(), name='institution-list'),
    path('admin/collaborations/', views.CollaborationList.as_view(), name='collaboration-list'),


    # --- 5. PUBLIC STATISTICS & DASHBOARD DATA ---
    path('stats/donors/', views.donor_statistics, name='donor-stats'),
    path('stats/events/', views.event_popularity, name='event-stats'),
    # FIXED: Added the missing route for the event-wide donation summary
    path('stats/event-funds/', views.event_donation_summary, name='event-funds-summary'),


    # --- 6. UNIVERSITY OFFERINGS ---
    path('events/', views.EventList.as_view(), name='event-list'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='event-delete'),
    
    path('programs/', views.ProgramList.as_view(), name='program-list'),
    path('programs/<int:pk>/delete/', views.ProgramDelete.as_view(), name='program-delete'),


    # --- 7. TRANSACTIONS & AWARDS ---
    path('awards/', views.AwardList.as_view(), name='award-list'),
    path('donations/', views.DonationList.as_view(), name='donation-list'),


    # --- 8. ALUMNUS SELF-SERVICE (New Dashboard Routes) ---
    path('my-profile/', views.my_profile_view, name='my-profile'),
    path('my-events/', views.my_events_view, name='my-events'),
    path('my-donations/', views.my_donations_view, name='my-donations'),
    path('join-event/<int:event_id>/', views.join_event, name='join-event'),
]