#!/usr/bin/env python3

import os
import urllib.parse

from flask import Flask, request, session, redirect, url_for
import requests


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY','iwonttellyou')

redirect_uri = 'https://'+os.environ.get('URL','localhost:5000')+'/callback'
client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
client_secret = os.environ.get('GOOGLE_SECRET')

auth_uri = 'https://accounts.google.com/o/oauth2/auth'
token_uri = 'https://accounts.google.com/o/oauth2/token'
scope = ('https://www.googleapis.com/auth/userinfo.profile',
         'https://www.googleapis.com/auth/userinfo.email')
profile_uri = 'https://www.googleapis.com/oauth2/v1/userinfo'


@app.route('/')
def index():
    if 'email' in session:
        return ('Hello <b>{}</b>. This version is deployed from drone.io.'
                '<a href="/logout">logout</a>').format(session['email'])
    else:
        return 'Please <a href="/login">login</a>'


@app.route('/logout')
def logout():
    session.pop('email', '')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    # Step 1
    params = dict(response_type='code',
                  scope=' '.join(scope),
                  client_id=client_id,
                  approval_prompt='auto',
                  redirect_uri=redirect_uri)
    url = auth_uri + '?' + urllib.parse.urlencode(params)
    return redirect(url)


@app.route('/callback')
def callback():
    if 'code' in request.args:
        # Step 2
        code = request.args.get('code')
        data = dict(code=code,
                    client_id=client_id,
                    client_secret=client_secret,
                    redirect_uri=redirect_uri,
                    grant_type='authorization_code')
        r = requests.post(token_uri, data=data)
        # Step 3
        access_token = r.json()['access_token']
        r = requests.get(profile_uri, params={'access_token': access_token})
        session['email'] = r.json()['email']
        return redirect(url_for('index'))
    else:
        return 'ERROR'

if __name__ == '__main__':
    app.run(debug=True)
