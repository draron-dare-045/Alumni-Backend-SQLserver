from rest_framework import generics, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Sum, Count
from .models import (
    Alumnidetails, Awards, Events, 
    Donations, Alumniprograms, Eventparticipation
)
from .serializers import (
    AlumniSerializer, AwardSerializer, EventSerializer, 
    DonationSerializer, ProgramSerializer, EventParticipationSerializer
)

# --- 1. Alumni Views (Now with Search & Security) ---
class AlumniList(generics.ListCreateAPIView):
    queryset = Alumnidetails.objects.all()
    serializer_class = AlumniSerializer
    
    # SECURITY: Anyone can view, but only logged-in users can ADD records
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # ADVANCED FEATURE: Search bar for Name, Degree, or Year
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['firstname', 'lastname', 'degree', 'graduationyear']

class AlumniDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alumnidetails.objects.all()
    serializer_class = AlumniSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# --- 2. COMPLEX QUERIES (Special Statistical Endpoints) ---

@api_view(['GET'])
def donor_statistics(request):
    """Reflects SQL Query #8: Top contributors"""
    # Using Django's 'annotate' to calculate sums across tables
    stats = (Alumnidetails.objects.annotate(total_donated=Sum('donations__amount'))
             .order_by('-total_donated')[:5])
    
    data = [
        {"name": f"{d.firstname} {d.lastname}", "total": d.total_donated or 0} 
        for d in stats
    ]
    return Response(data)

@api_view(['GET'])
def event_popularity(request):
    """Reflects SQL Query #9: Event participation counts"""
    events = Events.objects.annotate(participant_count=Count('eventparticipation'))
    data = [
        {"event": e.eventname, "participants": e.participant_count} 
        for e in events
    ]
    return Response(data)


# --- 3. Standard API Views ---
class AwardList(generics.ListCreateAPIView):
    queryset = Awards.objects.all()
    serializer_class = AwardSerializer

class EventList(generics.ListCreateAPIView):
    queryset = Events.objects.all()
    serializer_class = EventSerializer

class DonationList(generics.ListCreateAPIView):
    queryset = Donations.objects.all()
    serializer_class = DonationSerializer

class ProgramList(generics.ListCreateAPIView):
    queryset = Alumniprograms.objects.all()
    serializer_class = ProgramSerializer