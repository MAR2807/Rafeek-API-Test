import pytest


# End points to Test plan: 
# 2	GET	/posts/{id}	Get one post: valid id returns 200, invalid id (0, 101, 99999) returns 404	P1
# 3	GET	/posts?userId={id}	Filtering: every result belongs to that user; an unknown user returns []	P1
# 4	POST	/posts	Create: 201, payload echoed back, new id returned	P1
# 5	PUT	/posts/{id}	Full update: 200, all fields replaced	P1
# 6	PATCH	/posts/{id}	Partial update: only the changed field differs	P1
# 7	DELETE	/posts/{id}	Delete: 200, empty body	P1
# 8	GET	/posts/{id}/comments and /comments?postId={id}	Nested route and filter return the same comments	P1
# 9	GET	/users	Only used to check that every post’s userId points to a real user	P1

# 1	GET	/posts	List all posts: count (100) and schema	P1

def test_get_all_posts(post_client):
    response = post_client.get_posts()
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
    response = post_client.get_post_by_id(1)
    assert response.status_code == 200

def test_get_invalid_post_by_id(post_client):
    response = post_client.get_post_by_id(929299292929)
    assert response.status_code == 404

def test_get_post_by_user_id(post_client):
    # existing user has id of 5, verified in postman
    response = post_client.get_all_posts_by_user_id(5)
    assert response.status_code == 200

    posts = response.json()
    # List of post Id's associated with this userID
    post_ids = {41,42,43,44,45,46,47,48,49,50}  # confirmed user has only these id's in postman

    ## for each post in response, check if they have the Id's
    for post in posts:
        assert post["id"] in post_ids
  