from requests import post, get, delete

# добавляем работу
print(post('http://localhost:5000/api/jobs', json={'team_leader': 1,
                                                   'job': 'Bah mars',
                                                   'work_size': 1,
                                                   'collaborators': 'he',
                                                   'is_finished': False}).json())
print()

# запрашиваем не существующую работу
print(get('http://localhost:5000/api/jobs/999').json())
# запрашиваем работу, которую только что создали
print(get('http://localhost:5000/api/jobs/12').json())
print()

# удаляем несуществующую работу
print(delete('http://localhost:5000/api/jobs/999').json())
# удаляем работу, которую только что создали
print(delete('http://localhost:5000/api/jobs/12').json())
print()

# выводим все работы
print(get('http://localhost:5000/api/jobs').json())
