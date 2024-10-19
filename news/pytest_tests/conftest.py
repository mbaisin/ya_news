from datetime import datetime, timedelta

import pytest
from django.test.client import Client

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def anonymous_user():
    return Client()


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Sample News Title',
        text='This is a sample news text.'
    )


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='This is a sample comment.'
    )


@pytest.fixture
def multiple_news():
    today = datetime.now()
    for i in range(10):
        News.objects.create(
            title=f'News {i}',
            text=f'This is news no. {i}.',
            date=today - timedelta(days=i)
        )


@pytest.fixture
def multiple_comments(news, author):
    today = datetime.now()
    for i in range(10):
        Comment.objects.create(
            news=news,
            author=author,
            text=f'This is comment no. {i}.',
            created=today - timedelta(days=i)
        )


@pytest.fixture
def form_data():
    return {
        'text': 'New comment',
    }
