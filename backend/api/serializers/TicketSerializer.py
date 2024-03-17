from rest_framework import serializers

from api.models import Ticket

class SubmitTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['notes', 'file']
        # Specify additional validation rules
        extra_kwargs = {
            'notes': {'required': True},
            'file': {'required': True}
        }

    


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'deadline', 'state']



class CreateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'deadline']


class FrViewTicketSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(read_only=True, source="created_by.username")
    assigned_to = serializers.CharField(read_only=True, source="assigned_to.username")
    

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'deadline', 'state','created_by', 'assigned_to', 'notes', 'file']

    




class AllTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'