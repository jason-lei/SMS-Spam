# #!/usr/bin/env python

from __future__ import print_function
import flask
import httplib2
from flask import Flask, render_template, json, request, redirect
from oauth2client import client
from gmail_functions import *
import pandas as pd
import uuid
import pickle
from googleapiclient.discovery import build

app = flask.Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/classify_text', methods=['POST'])
def classify_text():

    _text = request.form['inputName']
    print(_text)
    from flask import Flask
    import pandas as pd
    d = {'v2': ("%s" %_text)}
    text_df = pd.DataFrame(data=d, index={0})
    vect =pickle.load(open('./model/vectorizer.pkl', "rb"))
    clf = pickle.load(open('./model/classifier.pkl', 'rb'))
    _output = clf.predict(vect.transform(text_df["v2"]))
    if _output[0] == 0: 
        class_label = 'ham i.e not spam'
        return render_template('results.html', classification=class_label) 
    else:
        class_label = 'spam'
        return render_template('results.html', classification=class_label) 

@app.route('/classify_email')
def classify_email():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        service = build('gmail', 'v1', credentials=credentials)
        results = service.users().labels().list(userId='me').execute()
        response = service.users().messages().list(userId='me',
                                               q='', maxResults=50).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        
        df = pd.DataFrame(data = None, columns=['message'])
        for i in range(50): #get first 50 emails
            df.loc[i] = GetMessage(service, 'me', messages[i]['id']) ['snippet']
        vect =pickle.load(open('./model/vectorizer.pkl', "rb"))
        clf = pickle.load(open('./model/classifier.pkl', 'rb'))
        df["label"] = clf.predict(vect.transform(df["message"]))
        df["class_label"] = df["label"].map({0:'ham', 1:"spam"})
        spam = df.loc[df.class_label=='spam']
        ham = df.loc[df.class_label=='ham']
        return render_template('view_email_results.html',
            tables=[spam.to_html(classes='spam'), ham.to_html(classes='ham')],
            titles = ['na', 'Spam Email', 'Ham Email'] )

@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/gmail.modify',
        redirect_uri=flask.url_for('oauth2callback', _external=True)
        )
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('classify_email'))

if __name__ == "__main__":
    app.secret_key = str(uuid.uuid4())
    app.run(debug=True, port=8080)

from oauth2client import client