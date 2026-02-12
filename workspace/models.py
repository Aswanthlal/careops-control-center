from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Workspace(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    timezone = models.CharField(max_length=50)
    contact_email = models.EmailField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('OWNER', 'Owner'),
        ('STAFF', 'Staff'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class Contact(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Conversation(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=(('open', 'Open'), ('closed', 'Closed')),
        default='open'
    )
    last_message_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.contact.name} Conversation"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.CharField(
        max_length=20,
        choices=(('system', 'System'), ('staff', 'Staff'), ('customer', 'Customer'))
    )
    channel = models.CharField(
        max_length=20,
        choices=(('email', 'Email'), ('sms', 'SMS'))
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:30]}"


class Service(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    duration_minutes = models.IntegerField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Booking(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=(
            ('confirmed', 'Confirmed'),
            ('completed', 'Completed'),
            ('no_show', 'No Show')
        ),
        default='confirmed'
    )

    def __str__(self):
        return f"{self.contact.name} - {self.service.name}"

class FormTemplate(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class FormSubmission(models.Model):
    form = models.ForeignKey(FormTemplate, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=(('pending', 'Pending'), ('completed', 'Completed')),
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.form.name} - {self.status}"

class InventoryItem(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    low_threshold = models.IntegerField()

    def __str__(self):
        return self.name

class InventoryUsage(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    amount_used = models.IntegerField()


class AutomationEvent(models.Model):
    event_type = models.CharField(max_length=50)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    related_object = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_type

class AutomationLog(models.Model):
    event = models.ForeignKey(AutomationEvent, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=(('success', 'Success'), ('failed', 'Failed'))
    )
    created_at = models.DateTimeField(auto_now_add=True)
