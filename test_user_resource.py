from requests import post, get, delete

# добавляем пользователя
print(post('http://localhost:5000/api/users', json={'name': 'no',
                                                    'surname': 'name',
                                                    'age': 1,
                                                    'position': 'eng',
                                                    'speciality': 'cook',
                                                    'address': 'home',
                                                    'email': 'a@a.com'}).json())
print()

# запрашиваем не существующего пользователя
print(get('http://localhost:5000/api/users/999').json())
# запрашиваем пользователя, которого только что создали
print(get('http://localhost:5000/api/users/3').json())
print()

# удаляем несуществующего пользователя
print(delete('http://localhost:5000/api/users/999').json())
# удаляем пользователя, которого только что создали
print(delete('http://localhost:5000/api/users/3').json())
print()

# выводим всех пользователей
print(get('http://localhost:5000/api/users').json())
