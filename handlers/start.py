import sqlite3

from aiogram import Dispatcher, types
from config import bot, MEDIA_DESTINATION
from const import START_MENU_TEXT
from database.sql_commands import Database
from keyboards.inline_buttons import start_menu_keyboard
from aiogram.utils.deep_linking import _create_link


async def start_button(message: types.Message):
    print(message)
    db = Database()
    db.sql_insert_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )

    command = message.get_full_command()
    print(command)
    if command[1] != "":
        link = await _create_link(link_type="start", payload=command[1])
        owner = db.sql_select_user_by_link(
            link=link
        )
        if owner['telegram_id'] == message.from_user.id:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="U cant use own reference link!!!"
            )
            return

        try:
            db.sql_insert_referral(
                owner=owner['telegram_id'],
                referral=message.from_user.id
            )
            db.sql_update_balance(
                owner=owner['telegram_id']
            )
            db.connection.commit()
            await bot.send_message(
                chat_id=owner['telegram_id'],
                text="U have new referral"
            )
        except sqlite3.IntegrityError:
            pass

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
