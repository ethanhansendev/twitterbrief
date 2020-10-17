from json import dumps, loads
from datetime import datetime
import requests
import psycopg2
import jwt
import os

def check_unique_credentials(username, email, cursor):
    '''
    Summary:
    Checks whether credentials are unique (for register)

    Parameters:
    username (string): Username submitted in form
    email (string): Email submitted in form
    cursor (PSQL Instance): Connection to psql database

    Returns:
    True or False
    '''
    checkExistingUserQuery = "select * from Users where username = %s or email = %s"
    cursor.execute(checkExistingUserQuery, (username, email))
    if len(cursor.fetchall()) > 0:
        return False
    return True

def register_user(username, email, hash, cursor):
    '''
    Summary:
    Inserts user into database
    '''
    registerUserQuery = "insert into Users(username, email, time, password) values (%s, %s, %s, %s)"
    cursor.execute(registerUserQuery, (username, email, datetime.now(), hash))

def get_followed_twitter_accounts(username):
    '''
    Summary:
    Get twitter accounts that the user follows
    '''
    payload = {'screen_name': username}
    token = os.environ.get("TWITTER_BEARER_TOKEN")
    auth = {'Authorization': token}
    response = requests.get('https://api.twitter.com/1.1/friends/ids.json', params=payload, headers=auth)
    return response

def add_accounts(accounts, cursor):
    '''
    Summary:
    Populates accounts table
    '''
    for account in accounts:
        payload = {'user_id': account}
        token = os.environ.get("TWITTER_BEARER_TOKEN")
        auth = {'Authorization': token}
        response = requests.get('https://api.twitter.com/1.1/users/show.json', params=payload, headers=auth)
        user = response.json()
        name = user['name']
        registerUserQuery = "insert into Accounts(id, username) values (%s, %s)"
        cursor.execute(registerUserQuery, (account, name))


def populate_followed_users(username, ids, cursor):
    '''
    Summary:
    Populates followed table
    '''
    for id in ids:
        registerUserQuery = "insert into Followed(username, account) values (%s, %s)"
        cursor.execute(registerUserQuery, (username, id))

def generate_token(username):
    '''
    Summary:
    Generates token from username using secret key
    '''
    return jwt.encode({'username': username}, os.environ.get("SECRET_TOKEN"), algorithm='HS256')


