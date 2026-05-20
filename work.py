import requests



global base_url
base_url = 'https://edozie-drf-project.onrender.com/'


try:
    import tokens
    global headers
    headers = {
            'Authorization': 'Bearer ' + tokens.access_token
        }
except ModuleNotFoundError as e:
    pass


#Make a Login request
def login(username, password):
    details = {
        'username': username,
        'password': password
    }
    try:
        resp = requests.post(base_url + 'blogpost/login/', json=details)
        access_token = resp.json()['access']
        refresh_token = resp.json()['refresh']
    except KeyError:
        print('Invalid Login Details!!!')
    else:
        with open('tokens.py', 'w') as tok:
            tok.write('access_token = ' + "'" + access_token + "'")
            tok.write('\n'*2)
            tok.write('refresh_token = ' + "'" + refresh_token + "'")
        print('Login Successful and Authentication tokens provided'.title())


def logout(refresh_token):
    data = {'refresh_token': refresh_token}
    resp = requests.post(base_url + 'blogpost/logout/', json=data)
    print(resp.json(), resp.status_code)
    print('Logged Out!!!')
    
#View profile
def profile_view():
    resp = requests.get(base_url + 'blogpost/profile/', headers=headers)
    print(resp.json())


#Create 
def create(title, content):
    data = {
        'title': title,
        'content': content,
    }
    resp = requests.post(base_url + 'create-post/', json=data, headers=headers)
    print(resp.json(), resp.status_code)


#Read
def read():
    resp = requests.get(base_url + f'posts/', headers=headers)
    print(resp.json())


def read_by_id(post_id):
    resp = requests.get(base_url + f'posts/{post_id}/comments/', headers=headers)
    print(resp.json())

#Update
def update(post_id, field_name, field_value):
    data = {
        field_name: field_value
    }
    resp = requests.patch(base_url + f'update-blogpost/{post_id}/', json=data, headers=headers)
    print(resp.status_code, resp.json())

#Delete
def delete(post_id):
    resp = requests.delete(base_url + f'delete-blogpost/{post_id}/', headers=headers)
    print(resp.status_code, resp.json())


def comments(post_id, commenter, comment):
    data = {
        'comment': comment,
        'commenter': commenter
    }
    resp = requests.post(base_url + f'blog/posts/{post_id}/comments/', headers=headers, json=data)
    print(resp.json(), resp.status_code)


def open_bank_account(phonenumber):
    data = {
        'phonenumber': phonenumber
    }
    resp = requests.post(base_url + 'bankapp/open-account/', headers=headers, json=data)
    print(resp.json(), resp.status_code)


def bank_profile():
    resp = requests.get(base_url + 'bankapp/bank-profile/', headers=headers)
    print(resp.json(), resp.status_code)


def transfer(receiver_account, amount, narration):
    data = {
        'receiver_account': receiver_account,
        'amount': amount,
        'narration': narration
    }
    resp = requests.post(base_url + 'bankapp/bank-transfer/', headers=headers, json=data)
    print(resp.json(), resp.status_code)
    

login('Osuamadi', 'Mmaduakolam_1996')
#bank_profile()
#logout(tokens.refresh_token)
#open_bank_account('09015175965')
#transfer('8161317871', 50000, "Testing")