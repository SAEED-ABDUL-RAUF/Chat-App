import json
import urllib.parse

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Group, GroupMessage

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = f'chat_{self.group_name}'
        self.user = self.scope['user']
        self.group = Group.objects.get(slug=self.group_name)

        #JOIN ROOM GROUP
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.group.online.add(self.user)

        onlineUsers = [user.username for user in self.group.online.all()]
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'online_list',
                'onlineUsers': onlineUsers
            })
        
        previous_messages = self.get_previous_messages()
        self.send(json.dumps({
            'type': 'previous_messages',
            'messages': previous_messages
        }))
        

    
    #LEAVE ROOM GROUP
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.group.online.remove(self.user)
        onlineUsers = [user.username for user in self.group.online.all()]
        self.group.online.remove(self.user)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'online_list',
                'onlineUsers': onlineUsers
            })
    
    #receive message from websocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        #send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username
            }
        )
        GroupMessage.objects.create(sender=self.user, group=self.group, content=message)


    #receive message from room group
    def chat_message(self, event):
        #send message to websocket
        self.send(text_data=json.dumps(event))
    def online_list(self, event):
        #send message to websocket
        self.send(text_data=json.dumps(event))
    
    def get_previous_messages(self):
        messages = GroupMessage.objects.filter(group=self.group).order_by('timestamp')
        return [{'username':message.sender.username, 'content':message.content} for message in messages]