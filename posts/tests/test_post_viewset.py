import pytest
import json
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.models import Post

@pytest.mark.django_db
def test_list_posts(api_client, create_post):
    create_post()
    url = reverse('post-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert isinstance(response.data, list)

@pytest.mark.django_db
def test_retrieve_post(api_client, create_post):
    post = create_post()
    url = reverse('post-detail', args=[post.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['title'] == post.title

@pytest.mark.django_db
def test_create_post(auth_client, post_payload, mock_image):
    post_payload['image'] = mock_image
    post_payload['tags'] = json.dumps(post_payload['tags'])
    post_payload['paragraphs'] = json.dumps(post_payload['paragraphs'])

    url = reverse('post-list')
    response = auth_client.post(url, post_payload, format='multipart')
    assert response.status_code == 201

@pytest.mark.django_db
def test_update_post(auth_client, create_post):
    post = create_post()
    url = reverse('post-detail', args=[post.id])
    data = {'title': 'Updated Title'}
    response = auth_client.patch(url, data)
    assert response.status_code == 200
    post.refresh_from_db()
    assert post.title == 'Updated Title'

@pytest.mark.django_db
def test_delete_post(auth_client, create_post):
    post = create_post()
    url = reverse('post-detail', args=[post.id])
    response = auth_client.delete(url)
    assert response.status_code == 204
    assert not Post.objects.filter(id=post.id).exists()

@pytest.mark.django_db
def test_filter_posts_by_tag(api_client, create_post):
    post1 = create_post(tags=['Cybersecurity'])
    post2 = create_post(tags=['AI'])
    url = reverse('post-list') + '?tag=Cybersecurity'
    response = api_client.get(url)
    assert response.status_code == 200
    assert all('Cybersecurity' in p['tags'] for p in response.data)


@pytest.mark.django_db
def test_create_post_with_invalid_file(auth_client, post_payload):
    fake_file = SimpleUploadedFile('malicious.txt', b'badcontent', content_type='text/plain')
    post_payload['image'] = fake_file
    post_payload['tags'] = json.dumps(post_payload['tags'])
    post_payload['paragraphs'] = json.dumps(post_payload['paragraphs'])

    url = reverse('post-list')
    response = auth_client.post(url, post_payload, format='multipart')
    assert response.status_code == 400
    assert 'image' in response.data