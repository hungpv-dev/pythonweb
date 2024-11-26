import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("page_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("page_updates", self.channel_name)

    async def send_page_link(self, event):
        page_link = event['page_link']
        await self.send(text_data=json.dumps({
            'page_link': page_link
        }))