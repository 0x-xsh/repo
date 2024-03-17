
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    
    TokenRefreshView,
)
from api.views import AssignTicket, CreateTicketAPIView, DeleteTicketAPIView, MarkNotificationsOpened, NotificationView, SigninView, SignupView, SubmitTicket, TicketListView

urlpatterns = [
    
    
    path('signin',SigninView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('create-ticket', CreateTicketAPIView.as_view(), name='create-ticket'),
    path('delete-ticket', DeleteTicketAPIView.as_view(), name='delete-ticket'),
    path('tickets',  TicketListView.as_view(), name='ticket-list'),
    path('assign-ticket',  AssignTicket.as_view(), name='assign-ticket'),
    path('submit-ticket',  SubmitTicket.as_view(), name='submit-ticket'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('notifications', NotificationView.as_view(), name='notifications-list'),
    path('mark-notifications-opened', MarkNotificationsOpened.as_view(), name='mark-notifications-opened'),
]
    
    
    
    
    
    
    
    

   
    


