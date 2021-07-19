from subprocess import run
from datetime import datetime

def run_console(command, key):
    return run([command, key], capture_output=True).stdout

stdout = run_console('ps', '-aux').decode()


def table_(stdout_data: str):
    """Парсин все таблицы и предоставление результата в как строка = список"""
    list_parsed = []
    list_stdout = stdout_data.split('\n')
    for stroka in list_stdout:
        stroka = stroka.split()
        while len(stroka) > 11:
            stroka[10] = stroka[10] + " " + stroka.pop()
        list_parsed.append(stroka)
    if list_parsed[len(list_parsed):] != []:
        return list_parsed[1:]
    else:
        return list_parsed[1:-1]

parsed_table = table_(stdout)

def users(parsed_table):
    """подсчёт юзеров из списка по нулевому индексу"""
    list_of_users = []
    for i in parsed_table:
        list_of_users.append(i[0])
    return set(list_of_users)

users = users(parsed_table)


print(f'Пользователи системы: {users}, \n'
      f'Процессов запущено: {len(parsed_table)}')

def count_process_by_users():
    """подсчёт количества процессов из списка по нулевому индексу"""
    dict_of_users = {}
    for user in users:
        dict_of_users[user] += int(stdout.count(user))
    return dict_of_users


def memory_mb():
    memory_precent = 0
    process = 0.0
    name_process = ''
    for i in parsed_table:
        memory_precent = float(i[3]) + memory_precent
        if float(i[3]) > process:
            process = float(i[3])
            name_process = i[10][:20]
    return round((memory_precent / 100) * 16000, 1), name_process


def cpu():
    cpu_precent = 0
    process = 0
    name_process = ''
    for i in parsed_table:
        cpu_precent = float(i[2]) + cpu_precent
        if float(i[2]) > process:
            process = float(i[2])
            name_process = i[10][:20]
    return round(cpu_precent, 1), name_process


print(f'Всего памяти используется: {memory_mb()[0]} mb\n'
      f'Больше всего памяти использует: {memory_mb()[1]}\n'
      f'Всего CPU используется: {cpu()[0]}%\n'
      f'Больше всего CPU использует: {cpu()[1]}')

with open(f'{datetime.now()}-scan.txt', 'w') as scan:
    scan.write(
                f'Пользователи системы: {users}, \n'
                f'Процессов запущено: {len(parsed_table)}'
                f'Всего памяти используется: {memory_mb()[0]} mb\n'
                f'Больше всего памяти использует: {memory_mb()[1]}\n'
                f'Всего CPU используется: {cpu()[0]}%\n'
                f'Больше всего CPU использует: {cpu()[1]}'
    )

