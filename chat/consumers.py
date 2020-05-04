import json
from .models import Message
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

User = get_user_model()
class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.last_10_messages()
        content = {
            'command' : 'messages',
            'messages' : self.messages_to_json(messages)
        }
        self.send_message(content)

    # Creating json out of multiple messages - used when retrieving messages
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    # Creating json out of one message
    def message_to_json(self, message):
        return {
            'author' : message.author.username,
            'content' : message.content,
            'timestamp' : str(message.timestamp)
        }

    # New message function
    def new_message(self, data):
        print('new message')
        print(data)
        author = data['from']
        if not data['message']:
            return None
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(
            author=author_user, 
            content=data['message'],
            )
        content = {
            'command' : 'new_message',
            'message' : self.message_to_json(message)
        }
        print('sdsds')
        return self.send_chat_message(content)
    
    # Creating statement for channel
    commands = {
        'fetch_messages' : fetch_messages,
        'new_message' : new_message,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        async_to_sync(self.accept())

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps(message))


# User = get_user_model()
# class ChatConsumer(WebsocketConsumer):

#     def fetch_messages(self, data):
#         messages = Message.last_10_messages(self.room_group_name)
#         content = {
#             'command': 'messages',
#             'messages': self.messages_to_json(messages)
#         }
#         self.send_message(content)

#     # Creating json out of multiple messages - used when retrieving messages
#     def messages_to_json(self, messages):
#         result = []
#         for message in messages:
#             result.append(self.message_to_json(message))
#         return result

#     # Creating json out of one message
#     def message_to_json(self, message):
#         return {
#             'author': message.author.username,
#             'content': message.content,
#             'timestamp': str(message.timestamp)
#         }

#     # New message function
#     def new_message(self, data):
#         print('new message')
#         print(data)
#         author = data['from']
#         if not data['message']:
#             print('none')
#             return None
#         author_user = User.objects.filter(username=author)[0]
#         message = Message.objects.create(
#             job=self.room_group_name,
#             author=author_user,
#             content=data['message'],
#         )
#         print(message)
#         content = {
#             'command': 'new_message',
#             'message': self.message_to_json(message)
#         }
#         print('sdsds')
#         return self.send_chat_message(content)

#     # Creating statement for channel
#     commands = {
#         'fetch_messages': fetch_messages,
#         'new_message': new_message,
#     }

#     def connect(self):
#         
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         print("\n\n\n\n\n\n\n\n\nself.room_group_name\n\n\n\n\n\n\n\n\n\n")
#         print(self.room_group_name)
#         print(self.channel_name)
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         async_to_sync(self.accept())

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     def receive(self, text_data):
#         data = json.loads(text_data)
#         self.commands[data['command']](self, data)

#     def send_chat_message(self, message):
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     def send_message(self, message):
#         self.send(text_data=json.dumps(message))

#     def chat_message(self, event):
#         message = event['message']

#         self.send(text_data=json.dumps(message))
