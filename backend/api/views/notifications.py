
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q  



from api.models import Notification
from api.permissions import IsFRUser
from api.serializers.NotificationSerializer import NotificationSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication

  













class NotificationView(APIView):
    
    permission_classes = [IsFRUser]  
    authentication_classes = [JWTAuthentication]  
    
    def get(self, request):
        try:
            
            user_id = request.user.id
            notifications = Notification.objects.filter(assistant_id=user_id)
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        


class MarkNotificationsOpened(APIView):
    permission_classes = [IsFRUser]  
    authentication_classes = [JWTAuthentication]  
    
    def put(self, request):
        try:
            notification_ids = request.data.get('notification_ids', [])
            
            # Fetch notifications with these IDs
            notifications = Notification.objects.filter(id__in=notification_ids)
            
            # Update each notification's opened attribute to True
            for notification in notifications:
                notification.opened = True
                notification.save()
            
            return Response({"message": "Notifications marked as opened successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)