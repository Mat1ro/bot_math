from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import bot, dp
from states.state import Test
from utils import QuestionAnswer


@dp.message_handler(commands=['test'], state="*")
async def cmd_test(msg: types.Message, state: FSMContext) -> None:
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    await bot.send_message(
        chat_id=msg.chat.id,
        text="Привет! Погнали посмотрим что у тебя там с математикой) Ответ присылай натуральными цифрами",
    )

    tasks_id = await QuestionAnswer.get_tasks_id(135)
    questions = await QuestionAnswer.get_questions(tasks_id)

    data = {
        'skill_id': 135,
        'task_id': 1,
        'counter_correct': 0,
        'index_question': 0,
        'questions': questions,
        "skills_info": {135: 0}
    }

    await state.update_data(data)

    await bot.send_message(
        chat_id=msg.chat.id,
        text=questions[0],
    )
    await Test.Question_answer.set()
