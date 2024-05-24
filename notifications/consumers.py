from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import get_template

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        # Called on connection.
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            self.close()
            return
        self.GROUP_NAME = f'user-notifications-{self.user.id}'
        async_to_sync(self.channel_layer.group_add)(
            self.GROUP_NAME, self.channel_name
        )
        self.accept()

    # def receive(self, text_data=None, bytes_data=None):
    #     # Called with either text_data or bytes_data for each frame
    #     # You can call:
    #     self.send(text_data="Hello world!")
    #     # Or, to send a binary frame:
    #     self.send(bytes_data="Hello world!")
    #     # Want to force-close the connection? Call:
    #     self.close()
    #     # Or add a custom WebSocket error code!
    #     self.close(code=4123)

    def disconnect(self, close_code):
        # Called when the socket closes
        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_discard)(
                self.GROUP_NAME, self.channel_name
            )

    def comment_interaction(self, event):
        # Called when someone has interacted w your comment
        html = get_template('notifications/partials/toast.html').render(
            context={ "notification": event['notification'], "link": event.get('link', None) }
        )
        self.send(text_data=html)
