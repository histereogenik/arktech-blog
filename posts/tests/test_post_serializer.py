import pytest
from posts.serializers import PostSerializer


@pytest.mark.django_db
def test_serializer_valid(post_payload, create_user, mock_image):
    user = create_user(is_staff=True)
    post_payload['image'] = mock_image
    serializer = PostSerializer(data=post_payload, context={'request': type('Request', (), {'user': user})})
    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_serializer_rejects_invalid_tags(post_payload, create_user):
    user = create_user(is_staff=True)
    post_payload['tags'] = ['InvalidTag']
    serializer = PostSerializer(data=post_payload, context={'request': type('Request', (), {'user': user})})
    assert not serializer.is_valid()
    assert 'tags' in serializer.errors

@pytest.mark.django_db
def test_serializer_allows_optional_paragraph_title(post_payload, create_user, mock_image):
    user = create_user(is_staff=True)
    post_payload['paragraphs'] = [{'content': 'Content without title'}]
    post_payload['image'] = mock_image
    serializer = PostSerializer(data=post_payload, context={'request': type('Request', (), {'user': user})})
    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_serializer_rejects_missing_paragraph_content(post_payload, create_user):
    user = create_user(is_staff=True)
    post_payload['paragraphs'] = [{'title': 'No content'}]
    serializer = PostSerializer(data=post_payload, context={'request': type('Request', (), {'user': user})})
    assert not serializer.is_valid()
    assert 'paragraphs' in serializer.errors

@pytest.mark.django_db
def test_serializer_handles_multiple_paragraphs(post_payload, create_user, mock_image):
    user = create_user(is_staff=True)
    post_payload['image'] = mock_image
    post_payload['paragraphs'] = [
        {'title': 'Intro', 'content': 'First part.'},
        {'title': 'Middle', 'content': 'Second part.'},
        {'content': 'Final part.'}
    ]

    serializer = PostSerializer(data=post_payload, context={'request': type('Request', (), {'user': user})})
    assert serializer.is_valid(), serializer.errors
    validated_data = serializer.validated_data
    assert len(validated_data['paragraphs']) == 3
    assert validated_data['paragraphs'][0]['title'] == 'Intro'
    assert validated_data['paragraphs'][1]['content'] == 'Second part.'

