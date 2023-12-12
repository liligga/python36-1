import sqlite3

from aiogram import Dispatcher, types
from config import bot, MEDIA_DESTINATION
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
    # with open(MEDIA_DESTINATION + "bot-photo.jpg", 'rb') as photo:
    #     await bot.send_photo(
    #         chat_id=message.from_user.id,
    #         photo=photo,
    #         caption=START_MENU_TEXT.format(
    #             user=message.from_user.first_name
    #         ),
    #         reply_markup=await start_menu_keyboard(),
    #         parse_mode=types.ParseMode.MARKDOWN
    #     )
    with open(MEDIA_DESTINATION + "drib_blink_bot.gif", 'rb') as animation:
        await bot.send_animation(
            chat_id=message.from_user.id,
            animation=animation,
            caption=START_MENU_TEXT.format(
                user=message.from_user.first_name
            ),
            reply_markup=await start_menu_keyboard(),
            parse_mode=types.ParseMode.MARKDOWN
        )


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
