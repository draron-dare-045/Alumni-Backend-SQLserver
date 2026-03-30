from rest_framework import generics, filters, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum, Count
from django.db import transaction
from django.contrib.auth.models import User

# JWT Imports
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import (
    Alumnidetails, 
    AlumniProfile, 
    Awards, Events, 
    Donations, Alumniprograms, Eventparticipation, 
    Externalinstitutions, Collaborationactivities
)
from .serializers import (
    AlumniSerializer, AwardSerializer, EventSerializer, 
    DonationSerializer, ProgramSerializer, EventParticipationSerializer,
    InstitutionSerializer, CollaborationSerializer
)

# --- 1. AUTHENTICATION & LOGIN ---
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['is_staff'] = self.user.is_staff
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# --- 2. REGISTRATION ---
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_alumni(request):
    data = request.data
    reg_no = data.get('registration_number')
    if not all([data.get('username'), data.get('password'), reg_no]):
        return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        alumnus_record = Alumnidetails.objects.get(registration_number=reg_no)
        if AlumniProfile.objects.filter(alumni_record=alumnus_record).exists():
            return Response({"error": "Account already exists."}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            user = User.objects.create_user(username=data['username'], password=data['password'])
            AlumniProfile.objects.create(user=user, alumni_record=alumnus_record, is_verified_profile=True)
            alumnus_record.isverified = True
            alumnus_record.save()
        return Response({"message": "Success"}, status=status.HTTP_201_CREATED)
    except Alumnidetails.DoesNotExist:
        return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

# --- 3. ALUMNI DIRECTORY (Staff/Public) ---
class AlumniList(generics.ListCreateAPIView):
    queryset = Alumnidetails.objects.all().order_by('-alumniid')
    serializer_class = AlumniSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['firstname', 'lastname', 'degree']

class AdminAlumniList(generics.ListCreateAPIView):
    queryset = Alumnidetails.objects.all().order_by('-alumniid')
    serializer_class = AlumniSerializer
    permission_classes = [permissions.AllowAny]

class AlumniDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alumnidetails.objects.all()
    serializer_class = AlumniSerializer
    permission_classes = [permissions.AllowAny]

# --- 4. PARTNERSHIPS ---
class InstitutionList(generics.ListCreateAPIView):
    queryset = Externalinstitutions.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [permissions.AllowAny]

class CollaborationList(generics.ListCreateAPIView):
    queryset = Collaborationactivities.objects.all().order_by('-activitydate')
    serializer_class = CollaborationSerializer
    permission_classes = [permissions.AllowAny]

# --- 5. UNIVERSITY OFFERINGS ---
class ProgramList(generics.ListCreateAPIView):
    queryset = Alumniprograms.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.AllowAny]

class EventList(generics.ListCreateAPIView):
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

class DonationList(generics.ListCreateAPIView):
    queryset = Donations.objects.all().order_by('-donationdate')
    serializer_class = DonationSerializer
    permission_classes = [permissions.AllowAny]

class AwardList(generics.ListAPIView):
    queryset = Awards.objects.all()
    serializer_class = AwardSerializer
    permission_classes = [permissions.AllowAny]

# --- 6. STATISTICS ---
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def donor_statistics(request):
    donors = (Alumnidetails.objects.annotate(total_donated=Sum('donations__amount'))
             .filter(total_donated__gt=0)
             .order_by('-total_donated')[:5])
    data = {
        "count": Alumnidetails.objects.count(),
        "total_amount": Donations.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
        "top_donors": [{"name": f"{d.firstname} {d.lastname}", "total": d.total_donated or 0} for d in donors]
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def event_popularity(request):
    events = Events.objects.annotate(participant_count=Count('eventparticipation'))
    data = [{"event": e.eventname, "participants": e.participant_count} for e in events]
    return Response(data)

# --- 7. OPERATIONS ---
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_alumnus_manual(request, pk):
    try:
        alumnus = Alumnidetails.objects.get(pk=pk)
        alumnus.isverified = True
        alumnus.save()
        return Response({"status": "Verified"})
    except Alumnidetails.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

class EventDelete(generics.DestroyAPIView):
    queryset = Events.objects.all()
    permission_classes = [permissions.AllowAny]

class ProgramDelete(generics.DestroyAPIView):
    queryset = Alumniprograms.objects.all()
    permission_classes = [permissions.AllowAny]

class CollaborationDelete(generics.DestroyAPIView):
    queryset = Collaborationactivities.objects.all()
    permission_classes = [permissions.AllowAny]

# --- 8. ALUMNUS SELF-SERVICE (Dashboard Views) ---

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def my_profile_view(request):
    """Returns the Alumnidetails record for the logged-in User"""
    try:
        profile_link = AlumniProfile.objects.get(user=request.user)
        alumnus = profile_link.alumni_record
        if request.method == 'GET':
            serializer = AlumniSerializer(alumnus)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = AlumniSerializer(alumnus, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except AlumniProfile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_events_view(request):
    """Returns all events with a flag indicating if the user is registered"""
    try:
        profile_link = AlumniProfile.objects.get(user=request.user)
        events = Events.objects.all().order_by('-eventdate')
        
        # Get IDs of events this specific alumnus is attending
        my_registrations = Eventparticipation.objects.filter(
            alumni=profile_link.alumni_record
        ).values_list('event_id', flat=True)
        
        serializer = EventSerializer(events, many=True)
        data = serializer.data
        for item in data:
            item['is_registered'] = item['eventid'] in my_registrations
            
        return Response(data)
    except AlumniProfile.DoesNotExist:
        return Response({"error": "Auth profile missing"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_donations_view(request):
    """Returns only donations made by the logged-in alumnus"""
    try:
        profile_link = AlumniProfile.objects.get(user=request.user)
        donations = Donations.objects.filter(alumni=profile_link.alumni_record).order_by('-donationdate')
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)
    except AlumniProfile.DoesNotExist:
        return Response([], status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def join_event(request, event_id):
    """Allows an alumnus to register for an event"""
    try:
        profile_link = AlumniProfile.objects.get(user=request.user)
        event = Events.objects.get(pk=event_id)
        
        # Check for existing registration
        if Eventparticipation.objects.filter(alumni=profile_link.alumni_record, event=event).exists():
            return Response({"message": "Already registered"}, status=status.HTTP_400_BAD_REQUEST)
            
        Eventparticipation.objects.create(
            alumni=profile_link.alumni_record,
            event=event,
            status='Confirmed'
        )
        return Response({"message": "Successfully registered"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
from django.http import JsonResponse

def event_donation_summary(request):
    return JsonResponse({"message": "Placeholder"})