import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def create_post_dict(userId, id, title, body):
    return {
        "userId": userId,
        "id": id,
        "title": title,
        "body": body,
    }



def get_posts():
    response = requests.get(f"{BASE_URL}/posts")
    return response

def get_post_by_id(id):
    response = requests.get(f"{BASE_URL}/posts/{id}")
    return response

def get_all_posts_by_user_id(id):
    response = requests.get(f"{BASE_URL}/posts?userId={id}")
    return response

def create_post(body):
    response = requests.post(f"{BASE_URL}/posts", json=body)
    return response

def update_post_by_id(id, body):
    response = requests.put(f"{BASE_URL}/posts/{id}", json=body)
    return response

def patch_post_field_by_id(id, field): #where field is a dict of key value pair
    response = requests.patch(f"{BASE_URL}/posts/{id}", json=field)
    return response

def delete_post_by_id(id):
    response = requests.delete(f"{BASE_URL}/posts/{id}")
    return response

def get_post_comments(id):
    response = requests.get(f"{BASE_URL}/posts/{id}/comments")
    return response

def get_comments_by_post_id(id):
    response = requests.get(f"{BASE_URL}/comments", params={"postId": id})
    return response

def get_users():
    response = requests.get(f"{BASE_URL}/users")
    return response