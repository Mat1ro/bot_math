import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import bot, dp
from xlsx_to_json import skill_to_json, task_to_json, current_dir


@dp.message_handler(commands=['start'], state="*")
async def cmd_start(msg: types.Message, state: FSMContext) -> None:
    try:
        await skill_to_json()
        await task_to_json()
        file_path = os.path.join(current_dir, "file.xlsx")
        if os.path.exists(file_path):
            os.remove(file_path)

    except FileNotFoundError as e:
        pass

    finally:
        await state.reset_state()
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
        await bot.send_message(
            chat_id=msg.chat.id,
            text="Привет! Это бот тренажер по математике у меня есть команда /test",
        )
