from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import bot, dp


@dp.message_handler(commands=['start'], state="*")
async def cmd_start(msg: types.Message, state: FSMContext) -> None:
    await state.reset_state()
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    await bot.send_message(
        chat_id=msg.chat.id,
        text="Привет! Это бот тренажер по математике у меня есть команда /test",
    )
