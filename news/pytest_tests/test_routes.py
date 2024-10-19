from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse


pytestmark = pytest.mark.django_db

@pytest.mark.parametrize(
    'url_name, parametrized_clint, expected_status, args',
    [
        ('news:home', pytest.lazy_fixture('anonymous_user'), HTTPStatus.OK, None),
        ('users:login', pytest.lazy_fixture('anonymous_user'), HTTPStatus.OK, None),
        ('users:logout', pytest.lazy_fixture('anonymous_user'), HTTPStatus.OK, None),
        ('users:signup', pytest.lazy_fixture('anonymous_user'), HTTPStatus.OK, None),
        ('news:detail', pytest.lazy_fixture('anonymous_user'), HTTPStatus.OK, pytest.lazy_fixture('news')),
        ('news:edit', pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND, pytest.lazy_fixture('comment')),
        ('news:edit', pytest.lazy_fixture('author_client'), HTTPStatus.OK, pytest.lazy_fixture('comment')),
        ('news:delete', pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND, pytest.lazy_fixture('comment')),
        ('news:delete', pytest.lazy_fixture('author_client'), HTTPStatus.OK, pytest.lazy_fixture('comment')),
    ]
)
def test_pages_availability(url_name, parametrized_clint, expected_status, args):
    url = reverse(url_name, args=(args.pk,)) if args else reverse(url_name)
    response = parametrized_clint.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url_name, args',
    (
        ('news:delete', pytest.lazy_fixture('comment')),
        ('news:edit', pytest.lazy_fixture('comment')),
    ),
)
def test_redirects(anonymous_user, url_name, args):
    login_url = reverse('users:login')
    url = reverse(url_name, args=(args.pk,))
    expected_url = f'{login_url}?next={url}'
    response = anonymous_user.get(url)
    assertRedirects(response, expected_url)
