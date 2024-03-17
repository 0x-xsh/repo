from channels.generic.websocket import WebsocketConsumer
import json

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        
        self.channel_layer.group_add('12', self.channel_name)
        self.accept()

    def disconnect(self, close_code):
         
        self.channel_layer.group_discard('12', self.channel_name)
        self.close()
        

    def receive(self, text_data):
        pass

    def notify_user(self, event):
        print('notified //////////////////')
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))