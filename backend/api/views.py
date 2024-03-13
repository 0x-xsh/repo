
from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q  

from api.serializers.SignupSerializer import SignupSerializer
from api.serializers.LoginSerializer import LoginSerializer
from api.serializers.TicketSerializer import AllTicketSerializer, FrViewTicketSerializer, SubmitTicketSerializer, TicketSerializer
from .models import Assistant, Ticket
from rest_framework.authentication import SessionAuthentication
from .permissions import IsFRUser, IsDZUser
from django.contrib.auth.hashers import check_password  
from django.utils.text import slugify


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            
            validated_data = serializer.validated_data
            
            if Assistant.objects.filter(username=validated_data['username']).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
           
            serializer.save()
            return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SigninView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = Assistant.objects.filter(username=username).first()
            
            if not user:
                return Response({'error' : 'User Doesn\'t exist'})
            
            
            if check_password(password, user.password):
                login(request, user)
                data = {'first_name' :user.first_name, 'last_name' :user.last_name}
                return Response({'message': 'Login successful', 'data' : data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid Password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SignOutView(APIView):
    authentication_classes = [SessionAuthentication]
   

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)




class CreateTicketAPIView(APIView):
    
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsFRUser]
    
    def post(self, request, format=None):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            ticket = Ticket(title = serializer.data['title'], description = serializer.data['description'], deadline = serializer.data['deadline'], state = 'open', created_by = request.user  )
            ticket.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TicketListView(APIView):
    authentication_classes = [SessionAuthentication]

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
    
    authentication_classes = [SessionAuthentication]
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
    authentication_classes = [SessionAuthentication]
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
    





