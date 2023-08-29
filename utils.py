import json
import os


class QuestionAnswer:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")
    skill_path = os.path.join(data_dir, "skill.json")
    task_path = os.path.join(data_dir, "task.json")

    @classmethod
    async def open_file(cls, path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    @classmethod
    async def get_tasks_id(cls, skill_id: int):
        file = await cls.open_file(cls.skill_path)
        for i in file:
            if i.get("skill_id") == skill_id:
                return i.get("task_id")

    @classmethod
    async def get_if_passed(cls, skill_id: int) -> int:
        file = await cls.open_file(cls.skill_path)
        for i in file:
            if i.get("skill_id") == skill_id:
                return i.get("if_passed")

    @classmethod
    async def get_if_failed(cls, skill_id: int):
        file = await cls.open_file(cls.skill_path)
        for i in file:
            if i.get("skill_id") == skill_id:
                return i.get("if_failed")

    @classmethod
    async def get_questions(cls, tasks: list[int]) -> list:
        questions = []
        file = await cls.open_file(cls.task_path)
        for i in tasks:
            for j in file:
                if j.get("task_id") == i:
                    questions.append(j["question"])
        return questions

    @classmethod
    async def is_correct(cls, task_id: int, answer: int) -> bool:
        file = await cls.open_file(cls.task_path)
        for i in file:
            if i["answer"] == answer and i["task_id"] == task_id:
                return True
        return False

    @classmethod
    async def is_finish(cls, msg, state) -> bool:
        state_data = await state.get_data()
        if state_data['skill_id'] == "fin":
            state_data['skills_info'].popitem()
            info = state_data['skills_info']
            result = ''
            for i in info:
                result += f"По навыку - {str(i)} ты решил {str(info[i])} задач\n"
            await msg.answer("Ты прошел тренировку, можешь снова начать по команде /test")
            await msg.answer(f"Твоя статистика {len(info)}\n\n{result}")
            await state.reset_state()
            return True
        return False


async def get_first_skill_id():
    with open(QuestionAnswer.skill_path, "r", encoding="utf-8") as file:
        file = json.load(file)
        for i in file:
            return i["skill_id"]