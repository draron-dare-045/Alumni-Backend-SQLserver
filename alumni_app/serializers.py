from rest_framework import serializers
from .models import (
    Alumnidetails, 
    Awards, 
    Events, 
    Donations, 
    Alumniprograms,
    Eventparticipation
)

class AwardSerializer(serializers.ModelSerializer):
    alumni_name = serializers.ReadOnlyField(source='alumniid.firstname')
    
    class Meta:
        model = Awards
        fields = ['awardid', 'awardname', 'awardyear', 'alumniid', 'alumni_name']

class DonationSerializer(serializers.ModelSerializer):
    alumni_name = serializers.ReadOnlyField(source='alumniid.firstname')
    event_name = serializers.ReadOnlyField(source='eventid.eventname')

    class Meta:
        model = Donations
        fields = ['donationid', 'amount', 'donationdate', 'alumniid', 'alumni_name', 'eventid', 'event_name']

class EventParticipationSerializer(serializers.ModelSerializer):
    alumni_name = serializers.ReadOnlyField(source='alumniid.firstname')
    event_name = serializers.ReadOnlyField(source='eventid.eventname')

    class Meta:
        model = Eventparticipation
        fields = ['participationid', 'role', 'alumniid', 'alumni_name', 'eventid', 'event_name']

class AlumniSerializer(serializers.ModelSerializer):
    # Added 'awards_set' source - usually Django's default related_name is lowercase modelname_set
    awards = AwardSerializer(many=True, read_only=True, source='awards_set')
    
    class Meta:
        model = Alumnidetails
        fields = [
            'alumniid', 
            'registration_number', # CRITICAL: Added for verification logic
            'firstname', 
            'lastname', 
            'gender', 
            'graduationyear', 
            'degree', 
            'email', 
            'phone', 
            'isverified',          # CRITICAL: Added to check status in React
            'awards'
        ]

class EventSerializer(serializers.ModelSerializer):
    total_donations = serializers.SerializerMethodField()

    class Meta:
        model = Events
        fields = ['eventid', 'eventname', 'eventtype', 'eventdate', 'location', 'total_donations']

    def get_total_donations(self, obj):
        from django.db.models import Sum
        total = Donations.objects.filter(eventid=obj).aggregate(Sum('amount'))['amount__sum']
        return total if total else 0

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumniprograms
        fields = '__all__'