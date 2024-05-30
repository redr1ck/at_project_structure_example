from http import HTTPStatus
from typing import List, Any

import pytest
from api.api_client import ApiClient
from api.objects_api import get_user, get_users
from assertions.assertions_base import (assert_status_code, assert_schema, assert_response_body_field,
                                        assert_response_body_fields, assert_user_not_found, assert_user_bad_request,
                                        assert_list_is_not_empty)
from models.user_models import UserResponse, UsersResponse


class TestUsers:
    """
        Тесты /user, /users
    """
    @pytest.fixture(scope="class")
    def client(self):
        return ApiClient()

    @staticmethod
    def get_gender_sorted_users_test_data(client) -> List[tuple[Any, str]]:
        """
        Возвращает тестовые данные для параметризации теста проверки результатов запроса users?gender={gender}
        :param client: объект http клиента
        :return: список кортежей вида [(user_id_1, gender), (user_id_2, gender), ... (user_id_n, gender)]
        """
        result = []
        for gender in ['male', 'female']:
            response = get_users(client, gender=gender)
            for user_id in response.json()['idList']:
                result.append((user_id, gender))
        return result

    sorted_user_ids_test_data = get_gender_sorted_users_test_data(ApiClient())

    @pytest.mark.parametrize("gender", ['male', 'female'])
    def test_users_gender_valid_response(self, client, gender):
        response = get_users(client, gender=gender)
        response_body = response.json()

        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, UsersResponse)
        assert_list_is_not_empty(response, response_body['idList'])

    @pytest.mark.parametrize("user_id, expected_gender", sorted_user_ids_test_data)
    def test_users_check_user_gender_and_id(self, client, user_id, expected_gender):
        user_response = get_user(client, user_id=str(user_id))
        user_object = user_response.json()['user']
        assert_response_body_field(user_response, user_object['gender'], expected_gender)
        assert_response_body_field(user_response, user_object['id'], user_id)

    @pytest.mark.xfail
    def test_users_request_without_gender_param(self, client):
        response = get_users(client)
        response_body = response.json()

        assert_status_code(response, HTTPStatus.BAD_REQUEST)
        # не проверяю тут схему, нужно уточнить по поводу обработки ошибок.
        # Основываюсь на предположении, что ошибки должны выводиться подобным образом.
        assert_response_body_field(response, response_body['isSuccess'], False)
        assert_response_body_field(response, response_body['errorCode'], 400)
        assert_response_body_field(response, response_body['errorMessage'],
                                   "Required String parameter 'gender' is not present")
        assert_response_body_field(response, response_body['idList'], [])

    @pytest.mark.parametrize('gender', [' ', 'magic', 'McCloud', '1', 'True'])
    @pytest.mark.xfail
    def test_users_invalid_gender(self, client, gender):
        response = get_users(client, gender=gender)
        response_body = response.json()

        assert_status_code(response, HTTPStatus.BAD_REQUEST)
        # во всех случаях логично было бы ожидать 400
        assert_response_body_field(response, response_body['isSuccess'], False)
        assert_response_body_field(response, response_body['errorCode'], 400)
        assert_response_body_field(response, response_body['errorMessage'],
                                   f"No enum constant com.coolrocket.app.api.test.qa.Gender.{gender}")
        assert_response_body_field(response, response_body['user'], None)

    def test_get_user_valid_id(self, client, request):
        user_id = '5'
        response = get_user(client, user_id=user_id)

        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, UserResponse)
        assert_response_body_fields(request, response, rmv_ids=False)

    @pytest.mark.parametrize("user_id", ['', ' ', 2147483647])
    def test_get_user_not_found(self, client, user_id):
        response = get_user(client, user_id=user_id)

        assert_user_not_found(response)

    # кейсы с отрицательными значениями добавил сюда, т.к. неизвестно допустимы ли такие id
    @pytest.mark.parametrize("user_id", [0, -2147483648, -2147483649, 2147483648, 'test', "//"])
    def test_user_invalid_id_bad_request(self, client, user_id):
        response = get_user(client, user_id=str(user_id))

        assert_user_bad_request(response, user_id)



