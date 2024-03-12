# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Assistant(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=110, unique=True)
    password = models.CharField(max_length=100)  
    is_fr = models.BooleanField(default=False)
    is_dz = models.BooleanField(default=False)




class Ticket(models.Model):
    title = models.CharField(max_length = 100)
    description = models.CharField(max_length = 100)
    notes = models.CharField(max_length = 100)
    file = models.FileField(null=True,)
    deadline = models.DateField()
    created_by = models.ForeignKey(Assistant, on_delete = models.CASCADE, related_name = 'created_by', null=True)
    assigned_to = models.ForeignKey(Assistant, on_delete = models.CASCADE, related_name = 'assigned_to', null=True)
    
    STATE_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    
    
    

class Notification(models.Model):
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    opened = models.BooleanField(default=False)
    
    





