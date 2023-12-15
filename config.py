from aiogram import Dispatcher, Bot
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
TOKEN = config("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
GROUP_ID = config("GROUP_ID")
ADMIN_ID = config("ADMIN_ID")
MEDIA_DESTINATION = config("MEDIA_DESTINATION")
