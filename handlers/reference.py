import re
import sqlite3

from aiogram import types, Dispatcher
from config import bot, ADMIN_ID
from const import REFERENCE_MENU_TEXT

from database.sql_commands import Database
import os
import binascii
from aiogram.utils.deep_linking import _create_link

from keyboards.inline_buttons import reference_menu_keyboard


async def reference_menu_call(call: types.CallbackQuery):
    db = Database()
    data = db.sql_reference_menu_data(
        tg_id=call.from_user.id
    )
    await bot.send_message(
        chat_id=call.from_user.id,
        text=REFERENCE_MENU_TEXT.format(
            user=call.from_user.first_name,
            balance=data['balance'],
            referral=data['total_referral']
        ),
        reply_markup=await reference_menu_keyboard()
    )


async def reference_link_call(call: types.CallbackQuery):
    db = Database()
    user = db.sql_select_user(
        tg_id=call.from_user.id
    )
    print(user)
    if not user['link']:
        token = binascii.hexlify(os.urandom(8)).decode()
        link = await _create_link(link_type="start", payload=token)
        db.sql_update_user_link(
            link=link,
            tg_id=call.from_user.id,
        )
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Here is ur new link: {link}"
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Here is ur old link: {user['link']}"
        )


def register_reference_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        reference_menu_call,
        lambda call: call.data == 'reference_menu'
    )
    dp.register_callback_query_handler(
        reference_link_call,
        lambda call: call.data == 'reference_link'
    )
