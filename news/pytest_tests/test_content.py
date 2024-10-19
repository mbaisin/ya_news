import pytest

from django.urls import reverse

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
        parametrized_client, news, form_expected
):
    url = reverse('news:detail', args=(news.pk,))
    response = parametrized_client.get(url)
    if form_expected:
        assert 'form' in response.context
        assert isinstance(response.context['form'], CommentForm)
    else:
        assert 'form' not in response.context


def test_news_list_has_less_than_10_items(author_client, multiple_news):
    response = author_client.get(reverse('news:home'))
    assert response.context['object_list'].count() <= NEWS_COUNT_ON_HOME_PAGE


def test_news_list_sorted_by_date(author_client, multiple_news):
    response = author_client.get(reverse('news:home'))
    news_list = response.context['object_list']
    dates = [news.date for news in news_list]
    assert dates == sorted(dates, reverse=True)


def test_comments_sorted_by_date(author_client, news, multiple_comments):
    response = author_client.get(reverse('news:detail', args=(news.pk,)))
    comment_list = response.context['news'].comment_set.order_by('created')
    dates = [comments.created for comments in comment_list]
    assert dates == sorted(dates)
