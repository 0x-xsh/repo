
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Ticket, Notification

@receiver(post_save, sender=Ticket)
def create_notification(sender, instance, created, **kwargs):
    if not created and instance.state == 'closed':
        
        message = f"Le Ticket '{instance.title}' est soumis."
        
        Notification.objects.create(assistant=instance.created_by, message=message)
        
        # channel_layer = get_channel_layer()
        
        
        # async_to_sync(channel_layer.group_send)(
        #     instance.created_by.id,
        #     {
        #         'type': 'notify_user',
        #         'message': 'msg'
        #     }
        # )
        