import json
import os

import openpyxl


async def skill_to_json() -> None:
    workbook = openpyxl.load_workbook('file.xlsx')
    sheet = workbook['Skill']

    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = {
            'skill_id': int(row[0]),
            'if_passed': row[1],
            'if_failed': row[2],
            'task_id': list(map(int, row[3].split(';')))
        }
        data.append(row_data)

    json_data = json.dumps(data, indent=4, ensure_ascii=False)

    with open('skill.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)


async def task_to_json() -> None:
    workbook = openpyxl.load_workbook('file.xlsx')
    sheet = workbook['Task']

    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = {
            'task_id': int(row[0]),
            'question': row[1],
            'answer': int(row[2]),
        }
        data.append(row_data)

    json_data = json.dumps(data, indent=4, ensure_ascii=False)

    with open('task.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)


