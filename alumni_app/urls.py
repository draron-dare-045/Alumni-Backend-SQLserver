from django.urls import path
from .views import (
    AlumniList, AlumniDetail, 
    AwardList, 
    EventList, 
    DonationList, 
    ProgramList
)

urlpatterns = [
    # Alumni Endpoints
    path('alumni/', AlumniList.as_view(), name='alumni-list'),
    path('alumni/<int:pk>/', AlumniDetail.as_view(), name='alumni-detail'),

    # Award Endpoints
    path('awards/', AwardList.as_view(), name='award-list'),

    # Event Endpoints
    path('events/', EventList.as_view(), name='event-list'),

    # Donation Endpoints
    path('donations/', DonationList.as_view(), name='donation-list'),

    # Program Endpoints
    path('programs/', ProgramList.as_view(), name='program-list'),
]