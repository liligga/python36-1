import re
import sqlite3

from aiogram import types, Dispatcher
from config import bot, ADMIN_ID
from const import PROFILE_TEXT
from database.sql_commands import Database
import random

from keyboards.inline_buttons import like_dislike_keyboard, my_profile_keyboard


async def my_profile_call(call: types.CallbackQuery):
    db = Database()
    profile = db.sql_select_profile(
        tg_id=call.from_user.id
    )
    if profile:
        with open(profile['photo'], 'rb') as photo:
            await bot.send_photo(
                chat_id=call.from_user.id,
                photo=photo,
                caption=PROFILE_TEXT.format(
                    nickname=profile['nickname'],
                    bio=profile['bio'],
                    age=profile['age'],
                    gender=profile['gender']
                ),
                parse_mode=types.ParseMode.MARKDOWN,
                reply_markup=await my_profile_keyboard()
            )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='U have no profile, please Register'
        )


async def random_profile_call(call: types.CallbackQuery):
    db = Database()
    profiles = db.sql_select_filter_profiles(
        tg_id=call.from_user.id
    )
    if profiles:
        random_profile = random.choice(profiles)
        with open(random_profile['photo'], 'rb') as photo:
            await bot.send_photo(
                chat_id=call.from_user.id,
                photo=photo,
                caption=PROFILE_TEXT.format(
                    nickname=random_profile['nickname'],
                    bio=random_profile['bio'],
                    age=random_profile['age'],
                    gender=random_profile['gender']
                ),
                parse_mode=types.ParseMode.MARKDOWN,
                reply_markup=await like_dislike_keyboard(owner_tg_id=random_profile['telegram_id'])
            )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='There is no profiles that u have not liked'
        )


async def like_detect_call(call: types.CallbackQuery):
    db = Database()
    owner = re.sub("like_", "", call.data)
    print(call.data)
    print(owner)
    try:
        db.sql_insert_like(
            owner=owner,
            liker=call.from_user.id
        )
    except sqlite3.IntegrityError:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='U liked this profile before'
        )
    finally:
        await random_profile_call(call=call)


async def delete_profile_call(call: types.CallbackQuery):
    db = Database()
    db.sql_delete_profile(
        tg_id=call.from_user.id
    )
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Deleted profile successfully'
    )


def register_profile_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        my_profile_call,
        lambda call: call.data == 'my_profile'
    )
    dp.register_callback_query_handler(
        random_profile_call,
        lambda call: call.data == 'random_profile'
    )
    dp.register_callback_query_handler(
        delete_profile_call,
        lambda call: call.data == 'delete_profile'
    )
    dp.register_callback_query_handler(
        like_detect_call,
        lambda call: "like_" in call.data
    )
