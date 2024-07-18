import json
import urllib.parse

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from .models import Group, GroupMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        self.room_group_name = f"chat_{self.group_name}"
        self.user = self.scope["user"]
        self.group = await database_sync_to_async(Group.objects.get)(
            slug=self.group_name
        )

        # JOIN ROOM GROUP
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # previous_messages = self.get_previous_messages()
        # self.send(json.dumps({
        #     'type': 'previous_messages',
        #     'messages': previous_messages
        # }))

    # LEAVE ROOM GROUP
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # receive message from websocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(message)

        # save data
        await database_sync_to_async(GroupMessage.objects.create)(
            sender=self.user, group=self.group, content=message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message, "user": self.user.username},
        )

    # receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    # def get_previous_messages(self):
    #     messages = GroupMessage.objects.filter(group=self.group).order_by('timestamp')
    #     return [{'username':message.sender.username, 'content':message.content} for message in messages]
