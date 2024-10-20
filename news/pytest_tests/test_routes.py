from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


pytestmark = pytest.mark.django_db

HOME_URL = pytest.lazy_fixture('home_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
DETAIL_URL = pytest.lazy_fixture('news_detail_url')
EDIT_URL = pytest.lazy_fixture('news_edit_url')
DELETE_URL = pytest.lazy_fixture('news_delete_url')
ANON_USER = pytest.lazy_fixture('anonymous_user')
NON_AUTHOR_USER = pytest.lazy_fixture('not_author_client')
AUTHOR_USER = pytest.lazy_fixture('author_client')


@pytest.mark.parametrize(
    'url_name, parametrized_client, expected_status',
    [
        (HOME_URL, ANON_USER, HTTPStatus.OK),
        (LOGIN_URL, ANON_USER, HTTPStatus.OK),
        (LOGOUT_URL, ANON_USER, HTTPStatus.OK),
        (SIGNUP_URL, ANON_USER, HTTPStatus.OK),
        (DETAIL_URL, ANON_USER, HTTPStatus.OK),
        (EDIT_URL, NON_AUTHOR_USER, HTTPStatus.NOT_FOUND),
        (EDIT_URL, AUTHOR_USER, HTTPStatus.OK),
        (DELETE_URL, NON_AUTHOR_USER, HTTPStatus.NOT_FOUND),
        (DELETE_URL, AUTHOR_USER, HTTPStatus.OK),
    ]
)
def test_pages_availability(url_name, parametrized_client, expected_status):
    """Доступность страниц для разных пользователей.

    Для анонимного пользователя доступны: главная страница,
    страница отдельной новости, страницы регистрации пользователей,
    входа в учётную запись и выхода из неё.

    Страницы удаления и редактирования комментария доступны автору комментария.

    Авторизованный пользователь не может зайти на страницы редактирования
    или удаления чужих комментариев (возвращается ошибка 404).
    """
    response = parametrized_client.get(url_name)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url_name',
    (
        DELETE_URL,
        EDIT_URL,
    ),
)
def test_redirects_for_anonymous_user(anonymous_user, url_name, login_url):
    """Проверка перенаправления неавторизированных пользователей.
    При попытке перейти на страницу редактирования или удаления комментария
    анонимный пользователь перенаправляется на страницу авторизации.
    """
    expected_url = f'{login_url}?next={url_name}'
    response = anonymous_user.get(url_name)
    assertRedirects(response, expected_url)
