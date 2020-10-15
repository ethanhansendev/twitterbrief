from flask import Flask, request
from json import dumps, loads
import requests
import hashlib
import jwt
import os

app = Flask(__name__)

data = {
    'users': [
        {
            'email': 'sample@email.com',
            'username': 'sampleusername',
            'password_hash': 'ajiodnsiocniwoencaffwfsae',
            'token': 'mfaopomasfmopcampmcpomcpoampo',
            'follows': [111,222,33]
        }
    ]
}

def check_valid_credentials(username, email):
    for user in data['users']:
        if user['email'] == email or user['username'] == username:
            return False
    return True

def generate_token(username):
    return jwt.encode({'username': username}, os.environ.get("SECRET_TOKEN"), algorithm='HS256')

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    username = request.form.get('username')

    if not check_valid_credentials(username, email):
        return dumps({ "Error": "Credentials already exist!" }), 500

    password = request.form.get('password')
    hash = hashlib.sha256("mypassword".encode()).hexdigest()

    payload = {'screen_name': username}
    token = os.environ.get("TWITTER_BEARER_TOKEN")
    auth = {'Authorization': token}
    response = requests.get('https://api.twitter.com/1.1/friends/ids.json', params=payload, headers=auth)

    if response.status_code != 200:
        print(response.json())
        return dumps({ "Error": "Invalid Twitter Account" }), 500

    follows = response.json()

    data['users'].append({
        'email': email,
        'username': username,
        'password_hash': hash,
        'follows': follows['ids']
    })
    return generate_token(username)


    

if __name__ == '__main__':
    app.run(port=5000)


'''
Sample Fetch Request
  const getUsers = () => {
    const url = '/get_users?screen_name=' + 'ethoshansen'
    fetch(url, {
      method: 'GET',
      mode: 'cors'
    })
  }
'''