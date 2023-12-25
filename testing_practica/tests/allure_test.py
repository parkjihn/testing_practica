
import pytest
import allure
from api_test import User, CRUD, JSONHandler


file_handler = JSONHandler('../db.json')


user_crud = CRUD('users', file_handler)

@allure.feature('Операции с пользователем')
class TestUserCRUD:
    @allure.story('Создание пользователя')
    def test_create_user(self):
        user_id = 'test_user'
        user = User(user_id, 'Тестовое имя', 'test@example.com')
        with allure.step(f'Создание пользователя с ID {user_id}'):
            assert user_crud.create(user_id, user) == True

    @allure.story('Чтение пользователя')
    def test_read_user(self):
        user_id = 'test_user'
        with allure.step(f'Чтение пользователя с ID {user_id}'):
            assert user_crud.read(user_id) is not None

    @allure.story('Обновление пользователя')
    def test_update_user(self):
        user_id = 'test_user'
        updated_info = {'name': 'Обновленное тестовое имя'}
        with allure.step(f'Обновление пользователя с ID {user_id}'):
            assert user_crud.update(user_id, updated_info) == True

    @allure.story('Удаление пользователя')
    def test_delete_user(self):
        user_id = 'test_user'
        with allure.step(f'Удаление пользователя с ID {user_id}'):
            assert user_crud.delete(user_id) == True