# #!/usr/bin/env python

from __future__ import print_function # In python 2.7
import sys
import flask
import httplib2
from flask import Flask, render_template, json, request, redirect
from flask_wtf import Form
from oauth2client import client
import uuid
from googleapiclient.discovery import build

app = flask.Flask(__name__)
#drive = build('drive', 'v2', http=http_auth)

@app.route('/')
def main():
    return render_template('index.html')

# @app.route('/spam-classifier')
# def showSignUp():
#     return render_template('classify.html')

@app.route('/classify', methods=['POST'])
def signUp():

    _text = request.form['inputName']
    print(_text)
    from flask import Flask
    import pandas as pd
    d = {'v2': ("%s" %_text)}
    text_df = pd.DataFrame(data=d, index={0})
    text_transformed = vectorizer.transform(text_df.v2)
    text_transformed = selector.transform(text_transformed).toarray()
    _output = clf.predict(text_transformed)
    print(_output)

    return render_template('results.html', classification=_output) 
@app.route('/test')
def test():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        service = build('gmail', 'v1', http_auth)
        #results = mail.files().list().execute()
        results = service.users().labels().list(userId='me').execute()
        return json.dumps(results)

@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/gmail.modify',
        redirect_uri=flask.url_for('oauth2callback', _external=True)
        #,
        #include_granted_scopes=True)
        )
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('test'))

if __name__ == "__main__":
    from sklearn.externals import joblib
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.feature_selection import SelectPercentile, f_classif
    clf = joblib.load('stored_pickles/model.pkl')
    selector = joblib.load('stored_pickles/selector.pkl')
    vocabulary_to_load =joblib.load('stored_pickles/vectorizer.pkl')
    vectorizer = TfidfVectorizer(vocabulary=vocabulary_to_load)
    vectorizer.fit(vocabulary_to_load)
    app.secret_key = str(uuid.uuid4())
    app.run(debug=True)
    # app.run(port=8080)

from oauth2client import client

flow = client.flow_from_clientsecrets(
    'client_secrets.json',
    scope='https://www.googleapis.com/auth/gmail.modify',
    redirect_uri='http://localhost:5000/oauth2callback')
flow.params['access_type'] = 'offline'         # offline access
flow.params['include_granted_scopes'] = True   # incremental auth