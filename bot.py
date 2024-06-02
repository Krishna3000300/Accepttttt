import logging
import asyncio
from os import environ
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

logging.basicConfig(level=logging.ERROR)

SESSION = environ.get("SESSION", "")
User = Client(name="AcceptUser", session_string=SESSION)


@User.on_message(filters.command(["run", "approve"], [".", "/rk"]))
async def approve(client, message):
    chat_id = message.chat.id
    await message.delete(True)
 
    while True:
        try:
            await client.approve_all_chat_join_requests(chat_id)
            break
        except FloodWait as e:
            logging.error(f"FloodWait: Sleeping for {e.value} seconds.")
            await asyncio.sleep(e.value)
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            break

    msg = await client.send_message(chat_id, "**Task Completed** ✓ **Approved All Pending Join Requests**")
    await asyncio.sleep(5)
    await msg.delete()


logging.info("Bot Started....")
User.run()
