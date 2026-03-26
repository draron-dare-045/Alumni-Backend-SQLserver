# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alumnidetails(models.Model):
    alumniid = models.AutoField(db_column='AlumniID', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dateofbirth = models.DateField(db_column='DateOfBirth', blank=True, null=True)  # Field name made lowercase.
    graduationyear = models.IntegerField(db_column='GraduationYear', blank=True, null=True)  # Field name made lowercase.
    degree = models.CharField(db_column='Degree', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    chapterid = models.IntegerField(db_column='ChapterID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'AlumniDetails'


class Alumniprograms(models.Model):
    programid = models.AutoField(db_column='ProgramID', primary_key=True)  # Field name made lowercase.
    programname = models.CharField(db_column='ProgramName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    programtype = models.CharField(db_column='ProgramType', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = True
        db_table = 'AlumniPrograms'


class Awards(models.Model):
    awardid = models.AutoField(db_column='AwardID', primary_key=True)  # Field name made lowercase.
    awardname = models.CharField(db_column='AwardName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    awardyear = models.IntegerField(db_column='AwardYear', blank=True, null=True)  # Field name made lowercase.
    alumniid = models.ForeignKey(Alumnidetails, models.DO_NOTHING, db_column='AlumniID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Awards'


class Collaborationactivities(models.Model):
    collaborationid = models.AutoField(db_column='CollaborationID', primary_key=True)  # Field name made lowercase.
    institutionid = models.ForeignKey('Externalinstitutions', models.DO_NOTHING, db_column='InstitutionID', blank=True, null=True)  # Field name made lowercase.
    activityname = models.CharField(db_column='ActivityName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    activitydate = models.DateField(db_column='ActivityDate', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = True
        db_table = 'CollaborationActivities'


class Donations(models.Model):
    donationid = models.AutoField(db_column='DonationID', primary_key=True)  # Field name made lowercase.
    alumniid = models.ForeignKey(Alumnidetails, models.DO_NOTHING, db_column='AlumniID', blank=True, null=True)  # Field name made lowercase.
    eventid = models.ForeignKey('Events', models.DO_NOTHING, db_column='EventID', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    donationdate = models.DateField(db_column='DonationDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Donations'


class Eventparticipation(models.Model):
    participationid = models.AutoField(db_column='ParticipationID', primary_key=True)  # Field name made lowercase.
    alumniid = models.ForeignKey(Alumnidetails, models.DO_NOTHING, db_column='AlumniID', blank=True, null=True)  # Field name made lowercase.
    eventid = models.ForeignKey('Events', models.DO_NOTHING, db_column='EventID', blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'EventParticipation'


class Events(models.Model):
    eventid = models.AutoField(db_column='EventID', primary_key=True)  # Field name made lowercase.
    eventname = models.CharField(db_column='EventName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    eventtype = models.CharField(db_column='EventType', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    eventdate = models.DateField(db_column='EventDate', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Events'


class Externalinstitutions(models.Model):
    institutionid = models.AutoField(db_column='InstitutionID', primary_key=True)  # Field name made lowercase.
    institutionname = models.CharField(db_column='InstitutionName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    institutiontype = models.CharField(db_column='InstitutionType', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ExternalInstitutions'


class Programparticipation(models.Model):
    participationid = models.AutoField(db_column='ParticipationID', primary_key=True)  # Field name made lowercase.
    alumniid = models.ForeignKey(Alumnidetails, models.DO_NOTHING, db_column='AlumniID', blank=True, null=True)  # Field name made lowercase.
    programid = models.ForeignKey(Alumniprograms, models.DO_NOTHING, db_column='ProgramID', blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ProgramParticipation'
