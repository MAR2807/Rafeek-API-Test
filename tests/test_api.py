import pytest

# Global variables:
NEW_POST = {"userId": 1, "title": "Test post title", "body": "Test post body"}

def test_get_all_posts(post_client):
    response = post_client.get_posts()
    assert response.status_code == 200

    # verify the response is a list and that all posts have the correct schema
    posts_data = response.json()

    assert isinstance(posts_data, list)
    assert len(posts_data) == 100

    # check the fields and types for every post
    for post in posts_data:
        assert set(post) == {"userId", "id", "title", "body"}
        assert isinstance(post["userId"], int)
        assert isinstance(post["id"], int)
        assert isinstance(post["title"], str)
        assert isinstance(post["body"], str)

def test_get_post_by_id(post_client):
    response = post_client.get_post_by_id(1)
    assert response.status_code == 200
    post = response.json()

    assert post["id"] == 1 # assert posts id is 1
    assert set(post) == {"userId", "id", "title", "body"} #assert post contains the required fields


@pytest.mark.parametrize("post_id", [0, 101, 99999])
def test_get_nonexistent_post_returns_404(post_client, post_id):
    response = post_client.get_post_by_id(post_id)
    assert response.status_code == 404
    assert response.json() == {}

def test_get_post_by_user_id(post_client):
    # existing user has id of 5, verified in postman
    response = post_client.get_all_posts_by_user_id(5)
    assert response.status_code == 200

    posts = response.json()
    # list of post ids associated with this user id
    post_ids = {41,42,43,44,45,46,47,48,49,50}  # confirmed user has only these ids in postman
    # verify user 5 owns exactly posts 41-50
    assert {p["id"] for p in posts} == post_ids, "user 5 should own exactly posts 41-50"
    assert all(p["userId"] == 5 for p in posts)


def test_get_posts_by_unknown_user(post_client):
    response = post_client.get_all_posts_by_user_id(9999)

    assert response.status_code == 200
    assert response.json() == []



def test_create_post_returns_created_resource(post_client):

    response = post_client.create_post(NEW_POST) # use existing global variable to create a post
    assert response.status_code == 201, response.text

    # turn response into json for validation
    created = response.json()

    # Verify that the created post echoes each submitted field
    for field, expected in NEW_POST.items():
        assert created[field] == expected, f"{field}: expected {expected!r}, got {created[field]!r}"
    assert isinstance(created["id"], int), "server should assign an integer id"


@pytest.mark.xfail(strict=True, reason="JSONPlaceholder does not validate POST payload fields")
def test_create_post_rejects_invalid_payload(post_client):
    response = post_client.create_post({})

    assert response.status_code == 400


@pytest.mark.xfail(strict=True, reason="JSONPlaceholder fakes writes; created posts are not persisted")
def test_created_post_is_retrievable(post_client):
    created = post_client.create_post(NEW_POST).json()

    response = post_client.get_post_by_id(created["id"])

    assert response.status_code == 200

def test_put_replaces_entire_post(post_client):
    updated = {"id": 1, "userId": 1, "title": "Updated title", "body": "Updated body"}
    response = post_client.update_post_by_id(1, updated)

    assert response.status_code == 200, response.text
    assert response.json() == updated

def test_patch_post_changes_only_requested_field(post_client):
    # save the original post so we can compare fields that should not change
    original = post_client.get_post_by_id(1)
    assert original.status_code == 200
    original_post = original.json()

    changed_title = "Patched title"
    response = post_client.patch_post_field_by_id(1, {"title": changed_title})
    assert response.status_code == 200

    patched_post = response.json()
    # only the title should be changed
    assert patched_post["title"] == changed_title
    assert patched_post["id"] == original_post["id"]
    assert patched_post["userId"] == original_post["userId"]
    assert patched_post["body"] == original_post["body"]


def test_delete_post(post_client):
    response = post_client.delete_post_by_id(1)
    assert response.status_code == 200
    # verify api returns an empty body after delete
    assert response.json() == {}


def test_post_comments_routes_return_same_comments(post_client):
    nested_response = post_client.get_post_comments(1)
    filtered_response = post_client.get_comments_by_post_id(1)

    assert nested_response.status_code == 200
    assert filtered_response.status_code == 200

    nested_comments = nested_response.json()
    filtered_comments = filtered_response.json()

    # nested route and filter should return the same comments
    assert nested_comments == filtered_comments
    assert nested_comments, "post 1 should have comments"
    assert all(comment["postId"] == 1 for comment in nested_comments)


def test_every_post_user_id_exists(post_client):
    posts_response = post_client.get_posts()
    users_response = post_client.get_users()

    assert posts_response.status_code == 200
    assert users_response.status_code == 200

    # create a set of valid user ids for quick lookup
    existing_user_ids = {user["id"] for user in users_response.json()}

    for post in posts_response.json():
        assert post["userId"] in existing_user_ids, f"post {post['id']} references missing user {post['userId']}"