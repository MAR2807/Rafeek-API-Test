import pytest

# Global variables:
NEW_POST = {"userId": 1, "title": "Test post title", "body": "Test post body"}

def test_get_all_posts(post_client):
    # Arrange: use the posts API client

    # Act
    response = post_client.get_posts()

    # Assert
    assert response.status_code == 200
    posts_data = response.json()

    assert isinstance(posts_data, list)
    assert len(posts_data) == 100

    for post in posts_data:
        assert set(post) == {"userId", "id", "title", "body"}
        assert isinstance(post["userId"], int)
        assert isinstance(post["id"], int)
        assert isinstance(post["title"], str)
        assert isinstance(post["body"], str)

def test_get_post_by_id(post_client):
    # Arrange
    post_id = 1

    # Act
    response = post_client.get_post_by_id(post_id)

    # Assert
    assert response.status_code == 200
    post = response.json()

    assert post["id"] == post_id
    assert set(post) == {"userId", "id", "title", "body"}


@pytest.mark.parametrize("post_id", [0, 101, 99999])
def test_get_nonexistent_post_returns_404(post_client, post_id):
    # Arrange
    # post_id is provided by pytest

    # Act
    response = post_client.get_post_by_id(post_id)

    # Assert
    assert response.status_code == 404
    assert response.json() == {}

def test_get_post_by_user_id(post_client):
    # Arrange
    user_id = 5
    post_ids = {41,42,43,44,45,46,47,48,49,50}

    # Act
    response = post_client.get_all_posts_by_user_id(user_id)

    # Assert
    assert response.status_code == 200

    posts = response.json()
    assert {p["id"] for p in posts} == post_ids, f"user {user_id} should own exactly posts 41-50"
    assert all(p["userId"] == user_id for p in posts)


def test_get_posts_by_unknown_user(post_client):
    # Arrange
    unknown_user_id = 9999

    # Act
    response = post_client.get_all_posts_by_user_id(unknown_user_id)

    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_create_post_returns_created_resource(post_client):
    # Arrange
    # NEW_POST contains the payload to create

    # Act
    response = post_client.create_post(NEW_POST)

    # Assert
    assert response.status_code == 201, response.text

    created = response.json()
    for field, expected in NEW_POST.items():
        assert created[field] == expected, f"{field}: expected {expected!r}, got {created[field]!r}"
    assert isinstance(created["id"], int), "server should assign an integer id"


@pytest.mark.xfail(strict=True, reason="JSONPlaceholder does not validate POST payload fields")
def test_create_post_rejects_invalid_payload(post_client):
    # Arrange
    invalid_payload = {}

    # Act
    response = post_client.create_post(invalid_payload)

    # Assert
    assert response.status_code == 400


@pytest.mark.xfail(strict=True, reason="JSONPlaceholder fakes writes; created posts are not persisted")
def test_created_post_is_retrievable(post_client):
    # Arrange
    created = post_client.create_post(NEW_POST).json()

    # Act
    response = post_client.get_post_by_id(created["id"])

    # Assert
    assert response.status_code == 200

def test_put_replaces_entire_post(post_client):
    # Arrange
    updated = {"id": 1, "userId": 1, "title": "Updated title", "body": "Updated body"}

    # Act
    response = post_client.update_post_by_id(1, updated)

    # Assert
    assert response.status_code == 200, response.text
    assert response.json() == updated

def test_patch_post_changes_only_requested_field(post_client):
    # Arrange
    original = post_client.get_post_by_id(1)
    assert original.status_code == 200
    original_post = original.json()

    changed_title = "Patched title"

    # Act
    response = post_client.patch_post_field_by_id(1, {"title": changed_title})

    # Assert
    assert response.status_code == 200

    patched_post = response.json()
    assert patched_post["title"] == changed_title
    assert patched_post["id"] == original_post["id"]
    assert patched_post["userId"] == original_post["userId"]
    assert patched_post["body"] == original_post["body"]


def test_delete_post(post_client):
    # Arrange
    post_id = 1

    # Act
    response = post_client.delete_post_by_id(post_id)

    # Assert
    assert response.status_code == 200
    assert response.json() == {}


def test_post_comments_routes_return_same_comments(post_client):
    # Arrange
    post_id = 1

    # Act
    nested_response = post_client.get_post_comments(post_id)
    filtered_response = post_client.get_comments_by_post_id(post_id)

    # Assert
    assert nested_response.status_code == 200
    assert filtered_response.status_code == 200

    nested_comments = nested_response.json()
    filtered_comments = filtered_response.json()

    assert nested_comments == filtered_comments
    assert nested_comments, "post 1 should have comments"
    assert all(comment["postId"] == 1 for comment in nested_comments)


def test_every_post_user_id_exists(post_client):
    # Arrange
    # use all posts and all users

    # Act
    posts_response = post_client.get_posts()
    users_response = post_client.get_users()

    # Assert
    assert posts_response.status_code == 200
    assert users_response.status_code == 200

    existing_user_ids = {user["id"] for user in users_response.json()}

    for post in posts_response.json():
        assert post["userId"] in existing_user_ids, f"post {post['id']} references missing user {post['userId']}"