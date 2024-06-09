import requests

def get_fullname(current_user):
    url = 'http://127.0.0.1:8000/user/get_fullname_by_username'
    params = {
        'username': current_user
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

print(get_fullname("admin"))