import sqlite3

from aiogram import Dispatcher, types
from config import bot
from const import START_MENU_TEXT
from database.sql_commands import Database
from keyboards.inline_buttons import start_menu_keyboard


async def start_button(message: types.Message):
    print(message)
    db = Database()
    db.sql_insert_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text=START_MENU_TEXT.format(
            user=message.from_user.first_name
        ),
        reply_markup=await start_menu_keyboard()
    )


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
