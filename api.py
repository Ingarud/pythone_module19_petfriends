import json
import os
from requests_toolbelt import MultipartEncoder
import requests
#from settings import valid_email, valid_password
import re

class PetFriends:
    def __init__(self, name='', animal_type='', age=''):
        self.base_url = 'https://petfriends.skillfactory.ru/'
        self.name = name
        self.animal_type = animal_type
        self.age = age

    def get_api_key(self, email, password) -> json:
        headers = {'email': email, 'password': password}

        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def __check_type(self):
        #проверить на присутсвие в списке()
        pattern = re.compile("^[a-zA-Zа-яА-ЯёЁ]+$")
        if pattern.match(self.animal_type) is None:
            return 400

    def __check_age(self):
        pattern = re.compile("^[0-9 ]+$")
        if pattern.match(self.age) is None:
            return 400




    def get_list_of_pets(self, auth_key:json, filter:str = '') -> json:
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url +'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key:json,  pet_photo:str) -> json:
        if self.__check_type() == 400 or self.__check_age() == 400:
            return 400, {}

        data = MultipartEncoder(
            fields={
                'name': self.name,
                'animal_type': self.animal_type,
                'age': self.age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type':data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id:str) -> json:
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str) -> json:

        headers = {'auth_key':auth_key['key']}

        data = {
            'name': self.name,
            'age': self.age,
            'animal_type': self.animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_without_photo(self, auth_key:json, ) -> json:

        if self.__check_type() == 400 or self.__check_age() == 400:
            return 400, {}

        data = MultipartEncoder(
            fields={
                'name': self.name,
                'animal_type': self.animal_type,
                'age': self.age,
                })

        headers = {'auth_key': auth_key['key'], 'Content-Type':data.content_type}
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_photo(self, auth_key: json, pet_photo: str, pet_id: str) -> json:

        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo, open('dog.jpg', 'rb'), 'image/jpg')})

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
