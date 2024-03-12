
from django.contrib import admin
from django.urls import include, path

from api.views import AssignTicket, CreateTicketAPIView, SignOutView, SigninView, SignupView, SubmitTicket, TicketListView

urlpatterns = [
    
    path('signout',SignOutView.as_view(), name='logout'),
    path('signin',SigninView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('create-ticket', CreateTicketAPIView.as_view(), name='create-ticket'),
    path('tickets',  TicketListView.as_view(), name='ticket-list'),
    path('assign-ticket',  AssignTicket.as_view(), name='assign-ticket'),
    path('submit-ticket',  SubmitTicket.as_view(), name='submit-ticket'),
    
    
    
    
    
    
    
    

   
    

]
