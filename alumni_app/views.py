from rest_framework import generics, filters, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum, Count
from django.db import transaction
from django.contrib.auth.models import User
from .models import (
    Alumnidetails, AlumniProfile, Awards, Events, 
    Donations, Alumniprograms, Eventparticipation
)
from .serializers import (
    AlumniSerializer, AwardSerializer, EventSerializer, 
    DonationSerializer, ProgramSerializer, EventParticipationSerializer
)

# --- CUSTOM PERMISSION ---
class IsVerifiedAlumnus(permissions.BasePermission):
    """
    Checks if the logged-in user has a linked and verified AlumniProfile.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.is_verified_profile
        )

# --- 1. AUTHENTICATION & REGISTRATION (The Automated Bridge) ---

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_alumni(request):
    """
    Creates a Django User and automatically links/verifies them to the SQL Record.
    Expects: username, password, email, registration_number
    """
    data = request.data
    reg_no = data.get('registration_number')
    
    if not all([data.get('username'), data.get('password'), reg_no]):
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 1. Look up the record in the legacy SQL Server registry
        alumnus_record = Alumnidetails.objects.get(registration_number=reg_no)
        
        # 2. Prevent duplicate accounts for the same registration number
        if AlumniProfile.objects.filter(alumni_record=alumnus_record).exists():
            return Response({"error": "This registration number is already linked to an account."}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Create User and Profile in a single safe transaction
        with transaction.atomic():
            user = User.objects.create_user(
                username=data['username'],
                email=data.get('email', ''),
                password=data['password']
            )

            AlumniProfile.objects.create(
                user=user,
                alumni_record=alumnus_record,
                is_verified_profile=True
            )
            
            # Update the status in the original SQL table
            alumnus_record.isverified = True
            alumnus_record.save()

        return Response({
            "message": f"Welcome {alumnus_record.firstname}! Your account is verified.",
            "status": "success"
        }, status=status.HTTP_201_CREATED)

    except Alumnidetails.DoesNotExist:
        return Response({"error": "Registration number not found in UoN records."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --- 2. Alumni Directory (SECURE: Verified Alumni Only) ---

class AlumniList(generics.ListAPIView):
    queryset = Alumnidetails.objects.all()
    serializer_class = AlumniSerializer
    permission_classes = [IsVerifiedAlumnus] # The "Walled Garden"
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['firstname', 'lastname', 'degree', 'graduationyear']

class AlumniDetail(generics.RetrieveAPIView):
    queryset = Alumnidetails.objects.all()
    serializer_class = AlumniSerializer
    permission_classes = [IsVerifiedAlumnus]


# --- 3. Public Statistics & Offerings (Anyone can see) ---

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def donor_statistics(request):
    stats = (Alumnidetails.objects.annotate(total_donated=Sum('donations__amount'))
             .order_by('-total_donated')[:5])
    data = [{"name": f"{d.firstname} {d.lastname}", "total": d.total_donated or 0} for d in stats]
    return Response(data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def event_popularity(request):
    events = Events.objects.annotate(participant_count=Count('eventparticipation'))
    data = [{"event": e.eventname, "participants": e.participant_count} for e in events]
    return Response(data)

class EventList(generics.ListAPIView):
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

class ProgramList(generics.ListAPIView):
    queryset = Alumniprograms.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.AllowAny]


# --- 4. Transactional Data (Basic Logged-in Users) ---

class AwardList(generics.ListAPIView):
    queryset = Awards.objects.all()
    serializer_class = AwardSerializer
    permission_classes = [permissions.IsAuthenticated]

class DonationList(generics.ListCreateAPIView):
    queryset = Donations.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]