from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Sum

from .models import (
    Alumnidetails, 
    Awards, 
    Events, 
    Donations, 
    Alumniprograms,
    Eventparticipation,
    Externalinstitutions,
    Collaborationactivities
)

# --- 1. AUTHENTICATION SERIALIZER ---
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['is_staff'] = self.user.is_staff
        return data

# --- 2. PARTNERSHIP SERIALIZERS ---
class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Externalinstitutions
        fields = '__all__'

class CollaborationSerializer(serializers.ModelSerializer):
    institution_name = serializers.ReadOnlyField(source='institutionid.institutionname')
    class Meta:
        model = Collaborationactivities
        fields = ['collaborationid', 'institutionid', 'institution_name', 'activityname', 'activitydate', 'description']

# --- 3. CORE ALUMNI & ACTIVITY SERIALIZERS ---
class AwardSerializer(serializers.ModelSerializer):
    firstname = serializers.ReadOnlyField(source='alumniid.firstname')
    lastname = serializers.ReadOnlyField(source='alumniid.lastname')
    class Meta:
        model = Awards
        fields = ['awardid', 'awardname', 'awardyear', 'alumniid', 'firstname', 'lastname']

class DonationSerializer(serializers.ModelSerializer):
    # Separate fields for portal detail views
    firstname = serializers.ReadOnlyField(source='alumniid.firstname')
    lastname = serializers.ReadOnlyField(source='alumniid.lastname')
    event_name = serializers.ReadOnlyField(source='eventid.eventname')
    
    # This field fixes the "Anonymous" issue in your Admin Table
    alumni_name = serializers.SerializerMethodField()

    class Meta:
        model = Donations
        fields = [
            'donationid', 'amount', 'donationdate', 
            'alumniid', 'firstname', 'lastname', 
            'alumni_name', 'eventid', 'event_name'
        ]

    def get_alumni_name(self, obj):
        """Combines firstname and lastname into the string expected by the frontend"""
        if obj.alumniid:
            return f"{obj.alumniid.firstname} {obj.alumniid.lastname}"
        return "Anonymous Donor"

class EventParticipationSerializer(serializers.ModelSerializer):
    firstname = serializers.ReadOnlyField(source='alumniid.firstname')
    lastname = serializers.ReadOnlyField(source='alumniid.lastname')
    event_name = serializers.ReadOnlyField(source='eventid.eventname')

    class Meta:
        model = Eventparticipation
        fields = ['participationid', 'role', 'alumniid', 'firstname', 'lastname', 'eventid', 'event_name']

class AlumniSerializer(serializers.ModelSerializer):
    awards = AwardSerializer(many=True, read_only=True, source='awards_set')
    class Meta:
        model = Alumnidetails
        fields = [
            'alumniid', 'registration_number', 'firstname', 'lastname', 
            'gender', 'graduationyear', 'degree', 'email', 'phone', 
            'isverified', 'awards'
        ]

class EventSerializer(serializers.ModelSerializer):
    total_donations = serializers.SerializerMethodField()
    class Meta:
        model = Events
        fields = ['eventid', 'eventname', 'eventtype', 'eventdate', 'location', 'total_donations']

    def get_total_donations(self, obj):
        total = Donations.objects.filter(eventid=obj).aggregate(Sum('amount'))['amount__sum']
        return float(total) if total else 0.0

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumniprograms
        fields = '__all__'