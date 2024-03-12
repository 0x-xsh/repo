# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Ticket, Notification

@receiver(post_save, sender=Ticket)
def create_notification(sender, instance, created, **kwargs):
    if created:
        print('notif //////////////////')
        message = f"Ticket '{instance.title} {instance.id}' has been submitted."
        # Save notification to the database
        Notification.objects.create(assistant=instance.created_by, message=message)
        # Send notification to WebSocket consumers
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications/{12}',
            {
                'type': 'notify_user',
                'message': message
            }
        )
