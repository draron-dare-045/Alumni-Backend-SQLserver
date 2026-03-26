from django.contrib import admin
from .models import (
    Alumnidetails, 
    AlumniProfile, 
    Awards, 
    Events, 
    Donations, 
    Alumniprograms, 
    Eventparticipation
)

# 1. THE BRIDGE: Manage the link between Users and SQL Records
@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    # What you see in the list view
    list_display = ('user', 'get_reg_no', 'is_verified_profile', 'date_verified')
    # Filter by verification status on the right sidebar
    list_filter = ('is_verified_profile', 'date_verified')
    # Search for users by username or their linked registration number
    search_fields = ('user__username', 'alumni_record__registration_number', 'user__email')
    
    # Custom method to show the Reg No in the list
    def get_reg_no(self, obj):
        return obj.alumni_record.registration_number if obj.alumni_record else "No Record Linked"
    get_reg_no.short_description = 'Registration Number'

# 2. THE MASTER LIST: Your Legacy SQL Server Records
@admin.register(Alumnidetails)
class AlumniDetailsAdmin(admin.ModelAdmin):
    list_display = ('alumniid', 'registration_number', 'firstname', 'lastname', 'degree', 'graduationyear', 'isverified')
    search_fields = ('registration_number', 'firstname', 'lastname', 'email')
    list_filter = ('degree', 'graduationyear', 'isverified')
    # Since this is a legacy table, we often make it 'read_only' in Admin to prevent accidental changes
    # Remove 'readonly_fields' if you want to edit these records directly
    # readonly_fields = ('alumniid', 'registration_number')

# 3. OTHER MODELS: Standard University Data
@admin.register(Awards)
class AwardsAdmin(admin.ModelAdmin):
    list_display = ('awardname', 'awardyear', 'alumniid')
    search_fields = ('awardname', 'alumniid__firstname')

@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('eventname', 'eventtype', 'eventdate', 'location')
    list_filter = ('eventtype', 'eventdate')

@admin.register(Donations)
class DonationsAdmin(admin.ModelAdmin):
    list_display = ('amount', 'donationdate', 'alumniid', 'eventid')
    list_filter = ('donationdate',)

@admin.register(Alumniprograms)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('programname', 'description')

@admin.register(Eventparticipation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('alumniid', 'eventid', 'role')