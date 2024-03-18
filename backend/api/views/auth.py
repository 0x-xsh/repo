
from api.models import Assistant
from api.serializers.SignupSerializer import SignupSerializer
from api.serializers.LoginSerializer import UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers.AssistantSerializer import AssistantSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


 






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