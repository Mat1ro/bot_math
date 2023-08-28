from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import bot, dp
from states.state import Test
from utils import QuestionAnswer


@dp.message_handler(state=Test.Question_answer)
async def question_answer(msg: types.Message, state: FSMContext) -> None:
    state_data = await state.get_data()

    task_id = state_data['task_id']

    if await QuestionAnswer.is_correct(task_id, int(msg.text)):
        await bot.send_message(chat_id=msg.chat.id, text="Молодец правильно")
        counter_correct = state_data['counter_correct'] + 1

        skill_info = state_data["skills_info"]
        skill_info[state_data['skill_id']] += 1

        await state.update_data({"skills_info": skill_info})
    else:
        await bot.send_message(chat_id=msg.chat.id, text="Не правильно, иди к следующей задаче")
        counter_correct = state_data['counter_correct']

    if state_data['index_question'] == 0:

        skill_id = state_data['skill_id']
        index_question = state_data['index_question'] + 1
        questions = state_data['questions']
        task_id += 1

    elif state_data['index_question'] == 1 and counter_correct >= 1:

        skill_id = state_data['skill_id']
        index_question = state_data['index_question'] + 1
        questions = state_data['questions']
        task_id += 1

    elif state_data['index_question'] == 1:

        index_question = 0
        counter_correct = 0
        skill_id = await QuestionAnswer.get_if_failed(state_data['skill_id'])

        skill_info = state_data["skills_info"]
        skill_info[skill_id] = 0
        await state.update_data({"skills_info": skill_info})

        await state.update_data({"skill_id": skill_id})
        if await QuestionAnswer.is_finish(msg, state):
            return

        tasks_id = await QuestionAnswer.get_tasks_id(skill_id)
        task_id = tasks_id[index_question]
        questions = await QuestionAnswer.get_questions(tasks_id)

    elif state_data['index_question'] == 2:

        skill_id = state_data['skill_id']
        index_question = state_data['index_question'] + 1
        questions = state_data['questions']
        task_id += 1

    elif state_data['index_question'] == 3 and counter_correct >= 3:

        index_question = 0
        counter_correct = 0
        skill_id = await QuestionAnswer.get_if_passed(state_data['skill_id'])
        await state.update_data({"skill_id": skill_id})

        skill_info = state_data["skills_info"]
        skill_info[skill_id] = 0
        await state.update_data({"skills_info": skill_info})

        if await QuestionAnswer.is_finish(msg, state):
            return

        tasks_id = await QuestionAnswer.get_tasks_id(skill_id)
        task_id = tasks_id[index_question]
        questions = await QuestionAnswer.get_questions(tasks_id)

    else:

        index_question = 0
        counter_correct = 0
        skill_id = await QuestionAnswer.get_if_failed(state_data['skill_id'])

        skill_info = state_data["skills_info"]
        skill_info[skill_id] = 0
        await state.update_data({"skills_info": skill_info})

        await state.update_data({"skill_id": skill_id})

        if await QuestionAnswer.is_finish(msg, state):
            return

        tasks_id = await QuestionAnswer.get_tasks_id(skill_id)
        task_id = tasks_id[index_question]
        questions = await QuestionAnswer.get_questions(tasks_id)

    await state.update_data({
        'skill_id': skill_id,
        'task_id': task_id,
        'counter_correct': counter_correct,
        'index_question': index_question,
        'questions': questions,
    })

    await bot.send_message(chat_id=msg.chat.id, text=questions[index_question])