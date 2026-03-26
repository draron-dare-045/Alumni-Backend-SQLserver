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
    # This pulls the actual name of the Alumnus for the award
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
    # This is an "Advanced Feature": It lists all awards belonging to this person
    awards = AwardSerializer(many=True, read_only=True, source='awards_set')
    
    class Meta:
        model = Alumnidetails
        fields = [
            'alumniid', 'firstname', 'lastname', 'gender', 
            'graduationyear', 'degree', 'email', 'phone', 'awards'
        ]

class EventSerializer(serializers.ModelSerializer):
    # Shows the total money raised for this specific event
    total_donations = serializers.SerializerMethodField()

    class Meta:
        model = Events
        fields = ['eventid', 'eventname', 'eventtype', 'eventdate', 'location', 'total_donations']

    def get_total_donations(self, obj):
        # This matches your SQL Complex Query for total donations per event
        from django.db.models import Sum
        total = Donations.objects.filter(eventid=obj).aggregate(Sum('amount'))['amount__sum']
        return total if total else 0

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumniprograms
        fields = '__all__'