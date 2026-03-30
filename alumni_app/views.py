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
    Alumnidetails, AlumniProfile, Awards, Events, 
    Donations, Alumniprograms, Eventparticipation, 
    Externalinstitutions, Collaborationactivities
)
from .serializers import (
    AlumniSerializer, AwardSerializer, EventSerializer, 
    DonationSerializer, ProgramSerializer, EventParticipationSerializer,
    InstitutionSerializer, CollaborationSerializer, MyTokenObtainPairSerializer
)

# --- 1. AUTHENTICATION ---
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
            # Link the new user to the existing alumni record
            AlumniProfile.objects.create(user=user, alumni_record=alumnus_record, is_verified_profile=True)
            alumnus_record.isverified = True
            alumnus_record.save()
        return Response({"message": "Success"}, status=status.HTTP_201_CREATED)
    except Alumnidetails.DoesNotExist:
        return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

# --- 3. DIRECTORY & LISTS ---
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

class InstitutionList(generics.ListCreateAPIView):
    queryset = Externalinstitutions.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [permissions.AllowAny]

class CollaborationList(generics.ListCreateAPIView):
    queryset = Collaborationactivities.objects.all().order_by('-activitydate')
    serializer_class = CollaborationSerializer
    permission_classes = [permissions.AllowAny]

class EventList(generics.ListCreateAPIView):
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

class ProgramList(generics.ListCreateAPIView):
    queryset = Alumniprograms.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.AllowAny]

class AwardList(generics.ListAPIView):
    queryset = Awards.objects.all()
    serializer_class = AwardSerializer
    permission_classes = [permissions.AllowAny]

class DonationList(generics.ListCreateAPIView):
    """Powers the Recent Contributions table in Admin"""
    queryset = Donations.objects.all().order_by('-donationdate')
    serializer_class = DonationSerializer
    permission_classes = [permissions.AllowAny]

# --- 4. STATISTICS & ANALYTICS ---
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def donor_statistics(request):
    """Calculates active donor count and total collection for Admin cards"""
    active_donors_count = Donations.objects.values('alumniid').distinct().count()
    
    donors = (Alumnidetails.objects.annotate(total_donated=Sum('donations__amount'))
             .filter(total_donated__gt=0)
             .order_by('-total_donated')[:5])
             
    data = {
        "count": active_donors_count,
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

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def event_donation_summary(request):
    summary = Events.objects.annotate(
        total_raised=Sum('donations__amount'),
        donor_count=Count('donations')
    ).order_by('-eventdate')
    data = []
    for event in summary:
        data.append({
            "eventid": event.eventid,
            "eventname": event.eventname,
            "total_raised": event.total_raised or 0,
            "donor_count": event.donor_count or 0,
            "goal": 1000000 
        })
    return Response(data)

# --- 5. OPERATIONS & SELF-SERVICE ---
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_donation(request):
    """
    Creates a new donation record. 
    Crucially links the donation to the Alumnidetails record via AlumniProfile.
    """
    try:
        # Get the profile that links the User to the Alumnus
        profile_link = AlumniProfile.objects.get(user=request.user)
        alumnus = profile_link.alumni_record
        
        data = request.data
        Donations.objects.create(
            alumniid=alumnus, # This ensures the name is associated
            eventid_id=data.get('eventid'),
            amount=data.get('amount'),
            donationdate=data.get('donationdate')
        )
        return Response({"message": "Donation Successful"}, status=status.HTTP_201_CREATED)
    except AlumniProfile.DoesNotExist:
        return Response({"error": "No Alumni Profile found for this user. Contribution cannot be named."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_donations_view(request):
    try:
        profile_link = AlumniProfile.objects.get(user=request.user)
        donations = Donations.objects.filter(alumniid=profile_link.alumni_record).order_by('-donationdate')
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)
    except AlumniProfile.DoesNotExist:
        return Response([], status=200)

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def my_profile_view(request):
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
        return Response({"error": "Profile not found"}, status=404)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_events_view(request):
    try:
        profile_link = AlumniProfile.objects.get(user=request.user)
        events = Events.objects.all().order_by('-eventdate')
        my_registrations = Eventparticipation.objects.filter(
            alumniid=profile_link.alumni_record
        ).values_list('eventid_id', flat=True)
        serializer = EventSerializer(events, many=True)
        data = serializer.data
        for item in data:
            item['is_registered'] = item.get('eventid') in my_registrations
        return Response(data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def join_event(request, event_id):
    try:
        profile_link = AlumniProfile.objects.get(user=request.user)
        event = Events.objects.get(pk=event_id)
        if Eventparticipation.objects.filter(alumniid=profile_link.alumni_record, eventid=event).exists():
            return Response({"message": "Already registered"}, status=400)
        Eventparticipation.objects.create(
            alumniid=profile_link.alumni_record,
            eventid=event,
            role='Attendee' 
        )
        return Response({"message": "Registered successfully"}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

# --- 6. HOUSEKEEPING & DELETES ---
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

