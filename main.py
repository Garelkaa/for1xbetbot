import time
from signature import bot, dp, db
from handlers.client import user
from handlers.admin import admin
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import handlers
import asyncio
from art import *
import utils

async def start():
    tprint("BY  BBYLFG")
    dp.include_router(user)
    dp.include_router(admin)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(db.update_ranking, 'cron', day='1,15', hour=0, minute=0)
    scheduler.start()
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(start())    
