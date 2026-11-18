import requests

BASE_URL = "https://jsonplaceholder.typicode.com"
REQUEST_TIMEOUT = 10

def create_post_dict(userId, id, title, body):
    return {
        "userId": userId,
        "id": id,
        "title": title,
        "body": body,
    }



def get_posts():
    response = requests.get(f"{BASE_URL}/posts", timeout=REQUEST_TIMEOUT)
    return response

def get_post_by_id(id):
    response = requests.get(f"{BASE_URL}/posts/{id}", timeout=REQUEST_TIMEOUT)
    return response

def get_all_posts_by_user_id(id):
    response = requests.get(f"{BASE_URL}/posts", params={"userId": id}, timeout=REQUEST_TIMEOUT)
    return response

def create_post(body):
    response = requests.post(f"{BASE_URL}/posts", json=body, timeout=REQUEST_TIMEOUT)
    return response

def update_post_by_id(id, body):
    response = requests.put(f"{BASE_URL}/posts/{id}", json=body, timeout=REQUEST_TIMEOUT)
    return response

def patch_post_field_by_id(id, field): #where field is a dict of key value pair
    response = requests.patch(f"{BASE_URL}/posts/{id}", json=field, timeout=REQUEST_TIMEOUT)
    return response

def delete_post_by_id(id):
    response = requests.delete(f"{BASE_URL}/posts/{id}", timeout=REQUEST_TIMEOUT)
    return response

def get_post_comments(id):
    response = requests.get(f"{BASE_URL}/posts/{id}/comments", timeout=REQUEST_TIMEOUT)
    return response

def get_comments_by_post_id(id):
    response = requests.get(f"{BASE_URL}/comments", params={"postId": id}, timeout=REQUEST_TIMEOUT)
    return response

def get_users():
    response = requests.get(f"{BASE_URL}/users", timeout=REQUEST_TIMEOUT)
    return response