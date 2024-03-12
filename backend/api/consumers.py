from channels.generic.websocket import WebsocketConsumer
import json

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        print('hello')
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        pass

    def notify_user(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))