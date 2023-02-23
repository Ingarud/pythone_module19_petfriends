from api import PetFriends
from settings import valid_email, valid_password
import re



def test_get_api_key_for_valid_user():
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    pf = PetFriends()

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(valid_email, valid_password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_api_key_for_invalid_user():
    """ Проверяем что запрос api ключа возвращает статус 400 при вводе некорректных данных"""

    invalid_email = "2314ewfe"
    invalid_password = '11222211'

    pf = PetFriends()

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result

    status, result = pf.get_api_key(invalid_email, invalid_password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

def test_get_api_key_for_invalid_password():
    """ Проверяем что запрос api ключа возвращает статус 400 при вводе неправильного пароля"""

    invalid_password = '11222211'

    pf = PetFriends()

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result

    status, result = pf.get_api_key(valid_email, invalid_password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


def test_get_all_pets(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    pf = PetFriends()


    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_my_pets(filter='my_pets'):
    """ Проверяем что запрос питомцев по фильтру my_pets до создания питомцев возвращает пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список питомцев и проверяем, что список пустой."""

    pf = PetFriends()

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) == 0


def test_add_new_pet_with_valid_data():
    """Проверяем что можно добавить питомца c фото с корректными данными"""

    pet_data = {
        'name': 'Мухтар',
        'animal_type': 'собака',
        'age': '2',
        'pet_photo': 'dog.jpg'
    }

    pf = PetFriends(pet_data['name'], pet_data['animal_type'], pet_data['age'])

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key,  pet_data['pet_photo'])

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == pet_data['name']



def test_add_new_pet_with_invalid_type():
    """Проверяем что можно добавить питомца c некорректными данными"""

    pet_data = {
        'name': "w432?",
        'animal_type': 'сqeак12а',
        'age': '2'
    }

    pf = PetFriends(pet_data['name'], pet_data['animal_type'], pet_data['age'])

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400



def test_add_new_pet_without_photo():
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    pet_data = {
        'name': 'Chak',
        'animal_type': 'dog',
        'age': '4'
    }

    pf = PetFriends(pet_data['name'], pet_data['animal_type'], pet_data['age'])

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == pet_data['name']

def test_add_photo(pet_photo = 'dog.jpg'):
    """Проверяем, что можно добавить фото питомца"""

    pf = PetFriends()
        # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']

    # Добавляем питомца
    status, result = pf.add_photo(auth_key, pet_photo,pet_id)
    print(result)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200


def test_get_all_my_pets(filter='my_pets'):
    """ Проверяем что запрос питомцев по фильтру my_pets после создания питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список питомцев и проверяем, что список не пустой."""

    pf = PetFriends()

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert len(result['pets']) > 0
    assert status == 200



def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    pf = PetFriends()

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Пушок", "собака", "2", "images/dog.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info():
    """Проверяем возможность обновления информации о питомце"""

    pet_data = {
        'name': 'Muhtar',
        'animal_type': 'dog',
        'age': '5'
    }

    pf = PetFriends(pet_data['name'], pet_data['animal_type'], pet_data['age'])

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'])

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == pet_data['name']
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")