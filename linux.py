from subprocess import run
import datetime



def  run_console(command, key):
    return run([command, key], capture_output=True).stdout


with open('proccess', 'w') as ps_aux:
    stdout = run_console('ps', 'aux').decode()
    ps_aux.write(stdout)


def table_(stdout_data: str):
    list_parsed = []
    list_stdout = stdout_data.split('\n')
    for stroka in list_stdout:

        stroka = stroka.split()
        while len(stroka) > 11:
            stroka[10] = stroka[10] + " " + stroka.pop()
        list_parsed.append(stroka)
    return list_parsed[:-1]


# for i in table_(stdout)[:10]:
#     print(i)

def users():
    list_of_users = []
    for _ in table_(stdout):
        list_of_users.append(_[0])
    return set(list_of_users)


users = users()

print(f'Пользователи системы: {users}, Процессов запущено: {len(table_(stdout))}')


def count_process_by_users():
    dict_of_users = {}
    for user in users:
        dict_of_users[user] += int(stdout.count(user))
    return dict_of_users


def memory_mb():
    memory_precent = 0
    process = 0.0
    for i in table_(stdout)[1:]:
        memory_precent = float(i[3]) + memory_precent
        if float(i[3]) > process:
            process = float(i[3])
            name_process = i[10][:20]
    return (memory_precent / 100) * 16000, name_process


def cpu():
    cpu_precent = 0
    process = 0
    for i in table_(stdout)[1:]:
        cpu_precent = float(i[2]) + cpu_precent
        if float(i[2]) > process:
            process = float(i[2])
            name_process = i[10][:20]
    return cpu_precent, name_process


print(f'Всего памяти используется: {memory_mb()[0]} mb Всего CPU используется: {cpu()[0]}% '
      f'Больше всего памяти использует: {memory_mb()[1]}'
      f' Больше всего CPU использует: {cpu()[1]}')