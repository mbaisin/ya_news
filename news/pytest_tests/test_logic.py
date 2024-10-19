import pytest
from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


pytestmark = pytest.mark.django_db


def test_author_can_post_comment(
        author_client, news, author, form_data
):
    url = reverse('news:detail', args=(news.pk,))
    comment_count_before = Comment.objects.count()
    author_client.post(url, data=form_data)
    assert Comment.objects.count() == comment_count_before + 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


def test_anonymous_user_cannot_post_comment(anonymous_user, news, form_data):
    url = reverse('news:detail', args=(news.pk,))
    comment_count_before = Comment.objects.count()
    anonymous_user.post(url, data=form_data)
    assert Comment.objects.count() == comment_count_before


def test_author_can_edit_comment(author_client, comment, form_data):
    url = reverse('news:edit', args=(comment.pk,))
    comment_count_before = Comment.objects.count()
    author_client.post(url, data=form_data)
    assert Comment.objects.count() == comment_count_before
    edited_comment = Comment.objects.get()
    assert edited_comment.text == form_data['text']


def test_non_author_cannot_edit_comment(not_author_client, comment, form_data):
    url = reverse('news:edit', args=(comment.pk,))
    comment_count_before = Comment.objects.count()
    not_author_client.post(url, data=form_data)
    assert Comment.objects.count() == comment_count_before
    edited_comment = Comment.objects.get()
    assert edited_comment.text == comment.text


def test_author_can_delete_comment(comment, author_client):
    url = reverse('news:delete', args=(comment.pk,))
    comment_count_before = Comment.objects.count()
    author_client.post(url)
    assert Comment.objects.count() == comment_count_before - 1


def test_non_author_cannot_delete_comment(not_author_client, comment):
    url = reverse('news:delete', args=(comment.pk,))
    comment_count_before = Comment.objects.count()
    not_author_client.post(url)
    assert Comment.objects.count() == comment_count_before


def test_user_cannot_post_comment_with_banned_words(author_client, news):
    url = reverse('news:detail', args=(news.pk,))
    form_data = {'text': f'{BAD_WORDS[0]}'}
    comment_count_before = Comment.objects.count()
    response = author_client.post(url, data=form_data)
    assert Comment.objects.count() == comment_count_before
    assert WARNING in response.context['form'].errors['text']
