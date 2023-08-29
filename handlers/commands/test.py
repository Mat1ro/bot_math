from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import bot, dp
from states.state import Test
from utils import QuestionAnswer, get_first_skill_id


@dp.message_handler(commands=['test'], state="*")
async def cmd_test(msg: types.Message, state: FSMContext) -> None:
    """
    Обработчик команды /test для начала тестирования пользователя.
    """
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    await bot.send_message(
        chat_id=msg.chat.id,
        text="Привет! Погнали, посмотрим, что у тебя там с математикой. Ответ присылай натуральными цифрами.",
    )

    # Получение первого навыка и первых вопросов
    skill_id = await get_first_skill_id()
    tasks_id = await QuestionAnswer.get_tasks_id(skill_id)
    questions = await QuestionAnswer.get_questions(tasks_id)

    """
    index_question - номер вопроса,
    questions - вопросы по данному skill_id
    skills_info - хранит статистику пользователя по навыкам
    """

    data = {
        'skill_id': skill_id,
        'task_id': 1,
        'counter_correct': 0,
        'index_question': 0,
        'questions': questions,
        "skills_info": {skill_id: 0}
    }

    await state.update_data(data)

    await bot.send_message(
        chat_id=msg.chat.id,
        text=questions[data['index_question']],
    )
    await Test.Question_answer.set()
