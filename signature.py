from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import config as cfg
from db.db import UserDB


storage = MemoryStorage()


bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(storage=storage)
db = UserDB('db/database.db')