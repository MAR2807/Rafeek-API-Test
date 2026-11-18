import pytest

from clients import posts_client


@pytest.fixture
def post_client():
    return posts_client

@pytest.fixture
def get_existing_post(post_client):
    response = post_client.get_post_by_id(1)
    assert response.status_code == 200
    return response