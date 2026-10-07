from django.db import models
from users.models import User, Role

class EventVenue(models.Model):
    venue_id = models.AutoField(primary_key=True, db_column='VenueId')
    venue_name = models.CharField(max_length=200, db_column='VenueName')
    capacity = models.IntegerField(null=True, blank=True, db_column='Capacity')
    address = models.CharField(max_length=500, null=True, blank=True, db_column='Address')
    
    class Meta:
        db_table = 'EventVenue'

class EventMaster(models.Model):
    event_id = models.AutoField(primary_key=True, db_column='EventId')
    event_name = models.CharField(max_length=200, db_column='EventName')
    event_type = models.CharField(max_length=100, db_column='EventType', null=True, blank=True)
    event_date = models.DateField(db_column='EventDate', null=True, blank=True)
    start_time = models.TimeField(db_column='StartTime', null=True, blank=True)
    end_time = models.TimeField(db_column='EndTime', null=True, blank=True)
    venue = models.ForeignKey(EventVenue, on_delete=models.SET_NULL, null=True, blank=True, db_column='VenueId')
    description = models.TextField(db_column='Description', null=True, blank=True)
    status = models.SmallIntegerField(db_column='Status', default=1) # 1: Upcoming, 2: Completed, 3: Cancelled
    organizer = models.CharField(max_length=200, db_column='Organizer', null=True, blank=True)
    contact_person = models.CharField(max_length=200, db_column='ContactPerson', null=True, blank=True)
    contact_phone = models.CharField(max_length=20, db_column='ContactPhone', null=True, blank=True)
    registration_start_date = models.DateField(db_column='RegStartDate', null=True, blank=True)
    registration_end_date = models.DateField(db_column='RegEndDate', null=True, blank=True)
    max_participants = models.IntegerField(db_column='MaxParticipants', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='CreatedBy', related_name='events_created')

    class Meta:
        db_table = 'EventMaster'

class EventParticipant(models.Model):
    event_participant_id = models.AutoField(primary_key=True, db_column='EventParticipantId')
    event = models.ForeignKey(EventMaster, on_delete=models.CASCADE, db_column='EventId')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserId')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, db_column='RoleId')
    registration_date = models.DateTimeField(auto_now_add=True, db_column='RegistrationDate')

    class Meta:
        db_table = 'EventParticipant'

class EventAttendance(models.Model):
    event_attendance_id = models.AutoField(primary_key=True, db_column='EventAttendanceId')
    event = models.ForeignKey(EventMaster, on_delete=models.CASCADE, db_column='EventId')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserId')
    attendance_status = models.SmallIntegerField(db_column='AttendanceStatus') # 1: Present, 2: Absent
    remarks = models.CharField(max_length=500, null=True, blank=True, db_column='Remarks')

    class Meta:
        db_table = 'EventAttendance'

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True, db_column='NotificationId')
    title = models.CharField(max_length=255, db_column='Title')
    message = models.TextField(db_column='Message')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserId', null=True)
    sent_date = models.DateTimeField(db_column='SentDate')
    is_read = models.BooleanField(default=False, db_column='IsRead')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')

    class Meta:
        db_table = 'Notification'
