import os
from api import PetFriends
from settings import *

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_not_valid_user(email=not_valid_email, password=valid_password):
    """ Проверяем что запрос api ключа при неправильном email возвращает статус 403 и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


def test_get_api_key_for_not_valid_password(email=valid_email, password=not_valid_password):
    """ Проверяем что запрос api ключа при неправильном пароле возвращает статус 403 и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Бобик', animal_type='дворкот',
                                     age='15', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "СуперБОБИК>", "котик", "13", "images/cat2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_successful_update_self_first_pet_info(name='Пушок', animal_type='Котик', age=4):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить имя, тип и возраст последнего в списке питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][len(my_pets['pets'])-1]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_simple_new_pet_with_valid_data(name='Шушик', animal_type='котяра', age='3'):
    """Проверяем что можно добавить питомца (без фото) с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)
   # pet_id = result['id']


    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_just_photo_pet_with_valid_data(pet_photo='images/cat2.jpg'):
    """Проверяем что можно добавить только фото питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_just_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 200
        assert 'pet_photo' in result

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии питомца с указанным ID
        raise Exception("There is no pet")


def test_delete_self_last_pet():
    """Проверяем возможность удаления последнего в списке питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список не пустой, то отправляем запрос на удаление последнего в списке питомца, ещё раз запрашиваем список своих питомцев,
    # после удаления, проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert pet_id not in my_pets.values()
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии питомца
        raise Exception("There is no pet")

def test_delete_self_first_pet():
    """Проверяем возможность удаления первого питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список не пустой, то отправляем запрос на удаление первого питомца из списка, ещё раз запрашиваем список своих питомцев,
    # после удаления, проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][len(my_pets['pets'])-1]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert pet_id not in my_pets.values()
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии питомца
        raise Exception("There is no pet")



def test_get_all_pets_with_not_valid_key(filter=''):
    """ Проверяем что происходит при попытке осуществить запрос всех питомцев c неправильными данными email и password.
    Для этого сначала пытаемся получить api ключ с некорректными данными и сохраняем результат в переменную auth_key.
    Если не удалось получить ключ или ключ неверный, то все хорошо, мы не сможем войти в систему (а так и должно быть).
    Если же удалось получить верный ключ, то получаем список всех питомцев, но предупреждаем, что НАЙДЕН "БАГ"-входа в систему с некорректными данными"""

    status, auth_key = pf.get_api_key(not_valid_email, not_valid_password)

    if status == 403:
        # Выкидываем исключение с текстом об ошибке
        assert auth_key == '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>403 Forbidden</title>\n<h1>Forbidden</h1>\n<p>This user wasn&#x27;t found in database</p>\n'
        #raise Exception("This user was not found in database")
    else:
        if status == 200:
            status, result = pf.get_list_of_pets(auth_key, filter)
            assert status == 200
            assert len(result['pets']) > 0
            raise Exception("FOUND BUG - login with incorrect data")
        else:
            raise Exception("Incorrect user data")


def test_add_new_pet_with_incorrect_age(name='Старик', animal_type='долгожитель',
                                     age='21', pet_photo='images/cat2.jpg'):
    """Т.к. в библиотеке api.py мы не проверяли ввод корректного значения возраста питомца (возраст не может быть отрицательным,
    и животные редко живут больше 20 лет,
    поэтому ограничим значение в пределах от 0 до 20), то будем отлавливать этот дефект системы. """

    # Готовимся к проведению теста:
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Выполняем проверку возраста питомца
    age = int(age)
    if (age <= 20) and age >=0:
        # Если все в порядке
        # Добавляем питомца
        age = str(age)
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
    else:
        # Выявляем баг системы когда возраст питомца не попадает в разумные пределы
        raise Exception("Incorrect age of pet")


def test_add_just_photo_pet_with_valid_data(pet_photo=''):
    """Проверяем, что происходит если не передаем значение параметра при попытке добавить фото питомца"""

    # Пытаемся получить полный путь изображения питомца и сохраняем в переменную pet_photo
    if pet_photo == '':
        raise Exception("File path not specified")
    else:
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        # Запрашиваем ключ api и сохраняем в переменую auth_key и список своих питомцев
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Если список не пустой, то пробуем добавить фото
        if len(my_pets['pets']) > 0:
            status, result = pf.add_pet_just_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
            # Проверяем что статус ответа = 200
            assert status == 200
            assert 'pet_photo' in result
        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии питомца с указанным ID
            raise Exception("There is no pet")