import pytest

from news.forms import CommentForm
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'parametrized_client, form_expected',
    (
        (pytest.lazy_fixture('anonymous_user'), False),
        (pytest.lazy_fixture('author_client'), True)
    ),
)
def test_news_page_contains_form(
        parametrized_client, news_detail_url, form_expected
):
    """Тест на доступность формы комментария.
    Для авторизированных пользователей форма комментария
    должна быть доступна.
    Для неавторизированных пользователей форма комментария
    не должна передаваться.
    """
    response = parametrized_client.get(news_detail_url)
    if form_expected:
        assert 'form' in response.context
        assert isinstance(response.context['form'], CommentForm)
    else:
        assert 'form' not in response.context


def test_news_list_has_less_than_10_items(
        author_client, home_url, multiple_news
):
    """Тест максимального количества новостей на стартовой странице."""
    response = author_client.get(home_url)
    assert response.context['object_list'].count() <= NEWS_COUNT_ON_HOME_PAGE


def test_news_list_sorted_by_date(author_client, home_url, multiple_news):
    """Тест на сортировку новостей на стартовой странице.
    Новости должны быть отсортированы от самой свежей к самой старой.
    Свежие новости в начале списка.
    """
    response = author_client.get(home_url)
    news_list = response.context['object_list']
    dates = [news.date for news in news_list]
    assert dates == sorted(dates, reverse=True)


def test_comments_sorted_by_date(
        author_client, news_detail_url, multiple_comments
):
    """Тест на сортировку комментариев на странице с новостью.
    Комментарии на странице отдельной новости должны быть отсортированы
    в хронологическом порядке: старые в начале списка, новые — в конце.
    """
    response = author_client.get(news_detail_url)
    comment_list = response.context['news'].comment_set.order_by('created')
    dates = [comments.created for comments in comment_list]
    assert dates == sorted(dates)
