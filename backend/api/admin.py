from django.contrib import admin

from api.models import Assistant, Notification, Ticket

# Register your models here.

admin.site.register(Assistant)
admin.site.register(Notification)
admin.site.register(Ticket)