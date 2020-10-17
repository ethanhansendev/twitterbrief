from flask import Flask, request
from json import dumps, loads
import requests
import psycopg2
import hashlib
import jwt
import os
from datetime import datetime

import auth


app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():

    # Get parameters
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    # Generate hashed password
    hash = hashlib.sha256(password.encode()).hexdigest()

    # Connect to database
    connection = psycopg2.connect(user="ethanhansen", password=os.environ.get("DATABASE_PASSWORD"), host="localhost", port="5432", database="twitterbrief")
    cursor = connection.cursor()


    if not auth.check_unique_credentials(username, email, cursor):
        return dumps({ "Error": "Credentials already exist!" }), 500

    # Get followed user
    response = auth.get_followed_twitter_accounts(username)

    if response.status_code != 200:
        print(response.json())
        return dumps({ "Error": "Invalid Twitter Account" }), 500

    
    # Add user to database
    auth.register_user(username, email, hash, cursor)

    follows = response.json()
    
    # Add followed accounts
    auth.add_accounts(follows['ids'], cursor)

    auth.populate_followed_users(username, follows['ids'], cursor)

    # Close database connection
    connection.commit()
    cursor.close()
    connection.close()

    # Return token
    return auth.generate_token(username)
    

@app.route('/login', methods=['GET'])
def login():
    # Get parameters
    username = request.args.get('username')
    password = request.args.get('password')

    # Generate hashed password
    hash = hashlib.sha256("mypassword".encode()).hexdigest()

    # Connect to database
    connection = psycopg2.connect(user="ethanhansen", password=os.environ.get("DATABASE_PASSWORD"), host="localhost", port="5432", database="twitterbrief")
    cursor = connection.cursor()

    findUserQuery = "select username, password from users where username = '{0}'".format(username)
    cursor.execute(findUserQuery)
    user = cursor.fetchone()

    if user[1] != hash:
       return {'Error': 'invalid credentials'}, 401

    return auth.generate_token(username)




if __name__ == '__main__':
    app.run(port=5000)
    