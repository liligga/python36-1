import sqlite3

from aiogram import types, Dispatcher
from config import bot
from keyboards import inline_buttons


async def start_questionnaire_call(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Python🐍 or Mojo🔥",
        reply_markup=await inline_buttons.start_questionnaire_keyboard()
    )


async def python_call(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="oh cool, Python Developer 🐍",
    )


async def mojo_call(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Dont lie to me!!!!",
    )


def register_questionnaire_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_questionnaire_call,
                                       lambda call: call.data == "start_questionnaire")
    dp.register_callback_query_handler(python_call,
                                       lambda call: call.data == "python")
    dp.register_callback_query_handler(mojo_call,
                                       lambda call: call.data == "mojo")
