from signature import bot, dp
from handlers.client import user
import handlers
import asyncio
from art import *
import utils

async def start():
    tprint("BY  BBYLFG")
    dp.include_router(user)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(start())    
