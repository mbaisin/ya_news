import pytest

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


pytestmark = pytest.mark.django_db


def test_author_can_post_comment(
        author_client, news, author, form_data, news_detail_url
):
    """Авторизованный пользователь может отправить комментарий."""
    comment_count_before = Comment.objects.count()
    author_client.post(news_detail_url, data=form_data)
    assert Comment.objects.count() == comment_count_before + 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


def test_anonymous_user_cannot_post_comment(
        anonymous_user, form_data, news_detail_url
):
    """Анонимный пользователь не может отправить комментарий."""
    comment_count_before = Comment.objects.count()
    anonymous_user.post(news_detail_url, data=form_data)
    assert Comment.objects.count() == comment_count_before


def test_author_can_edit_comment(author_client, news_edit_url, form_data):
    """Авторизованный пользователь может редактировать свои комментарии."""
    comment_count_before = Comment.objects.count()
    author_client.post(news_edit_url, data=form_data)
    assert Comment.objects.count() == comment_count_before
    edited_comment = Comment.objects.get()
    assert edited_comment.text == form_data['text']


def test_non_author_cannot_edit_comment(
        not_author_client, news_edit_url, comment, form_data
):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    comment_count_before = Comment.objects.count()
    not_author_client.post(news_edit_url, data=form_data)
    assert Comment.objects.count() == comment_count_before
    edited_comment = Comment.objects.get()
    assert edited_comment.text == comment.text


def test_author_can_delete_comment(news_delete_url, author_client):
    """Авторизованный пользователь может удалить свои комментарии."""
    comment_count_before = Comment.objects.count()
    author_client.post(news_delete_url)
    assert Comment.objects.count() == comment_count_before - 1


def test_non_author_cannot_delete_comment(not_author_client, news_delete_url):
    """Авторизованный пользователь не может удалить чужие комментарии."""
    comment_count_before = Comment.objects.count()
    not_author_client.post(news_delete_url)
    assert Comment.objects.count() == comment_count_before


def test_user_cannot_post_comment_with_banned_words(
        author_client, news_detail_url
):
    """Контроль запрещенных слов.
    Авторизованный пользователь не может опубликовать
    комментарий с запрещенными словами. Форма возвращает ошибку.
    """
    form_data = {'text': f'{BAD_WORDS[0]}'}
    comment_count_before = Comment.objects.count()
    response = author_client.post(news_detail_url, data=form_data)
    assert Comment.objects.count() == comment_count_before
    assert WARNING in response.context['form'].errors['text']
