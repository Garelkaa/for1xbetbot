import time
from signature import bot, dp
from handlers.client import user
from handlers.admin import admin
import handlers
import asyncio
from art import *
import utils

async def start():
    tprint("BY  BBYLFG")
    dp.include_router(user)
    dp.include_router(admin)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(start())    
