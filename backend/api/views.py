
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q  

from api.serializers.SignupSerializer import SignupSerializer
from api.serializers.LoginSerializer import UserLoginSerializer


from api.serializers.TicketSerializer import AllTicketSerializer, CreateTicketSerializer, FrViewTicketSerializer, SubmitTicketSerializer, TicketSerializer
from api.serializers.AssistantSerializer import AssistantSerializer
from api.serializers.NotificationSerializer import NotificationSerializer
from .models import Assistant, Notification, Ticket
from .permissions import IsFRUser, IsDZUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

  

from rest_framework.permissions import IsAuthenticated


from rest_framework_simplejwt.views import TokenObtainPairView





class SignupView(APIView):
    def post(self, request):
        if Assistant.objects.filter(username=validated_data['username']).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            
            validated_data = serializer.validated_data
            
            

            serializer.save()
            return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SigninView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': AssistantSerializer(user).data
            }, status=status.HTTP_200_OK) 
            
        return Response({"error" : serializer.errors['non_field_errors'][0]}, status=status.HTTP_400_BAD_REQUEST)


class CreateTicketAPIView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFRUser]
    
    def post(self, request, format=None):
        serializer = CreateTicketSerializer(data=request.data)
        if serializer.is_valid():
            ticket = Ticket(title = serializer.data['title'], description = serializer.data['description'], deadline = serializer.data['deadline'], state = 'open', created_by = request.user  )
            ticket.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteTicketAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFRUser]  
    
    def delete(self, request, format=None):
        ticket_id = request.data.get('id')  
        
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.delete()
            return Response({"message": "Ticket deleted successfully."}, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class TicketListView(APIView):
    
    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None):
        current_user = request.user
        
        
        tickets = Ticket.objects.all()
        serializer = FrViewTicketSerializer
      
        if IsDZUser().has_permission(request):
            
            tickets = tickets.filter(Q(state='open') | Q(assigned_to=current_user))
            serializer = TicketSerializer
            
        
        closed_tickets = [ticket for ticket in tickets if ticket.state == 'closed']
        progress_tickets = [ticket for ticket in tickets if ticket.state == 'in_progress']
        open_tickets = [ticket for ticket in tickets if ticket.state == 'open']

        
        
        closed_tickets_serializer = serializer(closed_tickets, many=True)
        open_tickets_serializer = serializer(open_tickets, many=True)
        progress_tickets_serializer = serializer(progress_tickets, many=True)

        
        return Response({
            'open_tickets': open_tickets_serializer.data,
            'closed_tickets': closed_tickets_serializer.data,
            'in_progress_tickets': progress_tickets_serializer.data
        })



class AssignTicket(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsDZUser]
    
    
    
    def put(self, request):
        ticket_id = request.query_params.get('id', None)
        
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
        except Ticket.DoesNotExist:
            return Response("Ticket not found", status=status.HTTP_404_NOT_FOUND)
        
        
        ticket.assigned_to = request.user
        ticket.state = 'in_progress'
        ticket.save()
        
        
        serializer = AllTicketSerializer(ticket)
        
        return Response(serializer.data)



class SubmitTicket(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsDZUser]
    
    def put(self, request):
        try:
            ticket_id = request.query_params.get('id', None)
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

        if ticket.assigned_to != request.user:
            return Response({"error": "You are not authorized to submit this ticket."}, status=status.HTTP_403_FORBIDDEN)

        serializer = SubmitTicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            ticket.state = 'closed'
            
            file = request.FILES.get('file')
            if file:
                file_name = f"ticket_number_{ticket_id}.zip"
                
                ticket.file.name = file_name
                
            
            notes = serializer.validated_data.get('notes', None)
            if notes:
                ticket.notes = notes
            
            
            ticket.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    





class NotificationView(APIView):
    
    permission_classes = [IsAuthenticated]  
    authentication_classes = [JWTAuthentication]  
    
    def get(self, request):
        try:
            
            user_id = request.user.id
            notifications = Notification.objects.filter(assistant_id=user_id)
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)