import os
import asyncio
import logging

from telethon import TelegramClient
from telethon import events

from dotenv import load_dotenv

load_dotenv()


"""Logger"""
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


"""API ID and hash from my.telegram.org to create a telegram client"""

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')

class UserFilterBot(TelegramClient):
    def __init__(self, session_name, api_id, api_hash):
        super().__init__(session_name, api_id, api_hash)
        self.add_event_handler(self.check_and_archive, events.NewMessage(incoming=True, func=lambda e: bool((not e.is_group or e.is_private))))

    async def loader(self): 
        await self.start()
        print("User Filter Bot started. Press Ctrl+C to stop.")
        await self.run_until_disconnected()
        
    """Check if the sender is in the contact list and if not, archive the chat and blacklist the user
        @param event: The event that triggered the function
    """
    async def check_and_archive(self, event):
        sender = await self.get_entity(event.sender_id)
        if not sender.bot:
            if not sender.contact:
                print("Sender {} not found in contacts".format(event.sender_id))
                await event.reply("You are not in my contact list.")
                sender = await self.get_entity(event.sender_id)
                chat = await self.get_entity(event.chat_id)
                # await event.blacklist_users(sender)
                await self.edit_folder(chat, 1)
                print("Blacklisted {}".format(sender))


async def main():
    client = UserFilterBot('session_name', api_id, api_hash)
    await client.loader()




if __name__ == '__main__':
    try: 
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Detected keyboard interrupt. Exiting...💀")
    


































    

