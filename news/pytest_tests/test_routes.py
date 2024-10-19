from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url_name, parametrized_client, expected_status',
    [
        (pytest.lazy_fixture('home_url'),
         pytest.lazy_fixture('anonymous_user'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('login_url'),
         pytest.lazy_fixture('anonymous_user'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('logout_url'),
         pytest.lazy_fixture('anonymous_user'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('signup_url'),
         pytest.lazy_fixture('anonymous_user'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('news_detail_url'),
         pytest.lazy_fixture('anonymous_user'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('news_edit_url'),
         pytest.lazy_fixture('not_author_client'),
         HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('news_edit_url'),
         pytest.lazy_fixture('author_client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('news_delete_url'),
         pytest.lazy_fixture('not_author_client'),
         HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('news_delete_url'),
         pytest.lazy_fixture('author_client'),
         HTTPStatus.OK),
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
        pytest.lazy_fixture('news_delete_url'),
        pytest.lazy_fixture('news_edit_url'),
    ),
)
def test_redirects_for_anonymous_user(anonymous_user, url_name, login_url):
    """
    При попытке перейти на страницу редактирования или удаления комментария
    анонимный пользователь перенаправляется на страницу авторизации.
    """
    expected_url = f'{login_url}?next={url_name}'
    response = anonymous_user.get(url_name)
    assertRedirects(response, expected_url)
