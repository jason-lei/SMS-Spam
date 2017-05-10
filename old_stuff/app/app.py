# #!/usr/bin/env python

from __future__ import print_function # In python 2.7
import sys
from flask import Flask, render_template, json, request, redirect
from flask_wtf import Form
import json

CLIENT_ID = "408758769479-r945hn2554a61dt28aht6t2t4mkm74n6.apps.googleusercontent.com"
CLIENT_SECRET = "H85RtLd8iVRXNRRjD6eHbN-_"
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

# @app.route('/spam-classifier')
# def showSignUp():
#     return render_template('classify.html')

@app.route('/classify', methods=['POST'])
def signUp():

    _text = request.form['inputName']
    from flask import Flask, jsonify
    import pickle
    #from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_selection import SelectPercentile, f_classif
    import pandas as pd
    d = {'message': ("%s" % _text)}
    
    print(_text)

    text_df = pd.DataFrame(data=d, index={0})
    print(text_df)
    vect =pickle.load(open('../model/vectorizer.pkl', "rb"))
    clf = pickle.load(open('../model/classifier.pkl', 'rb'))
    #vectorizer2 = TfidfVectorizer(vocabulary=vocabulary_to_load)
    #vectorizer2.fit(vocabulary_to_load)
    #text_transformed = vectorizer2.transform(text_df)
    #_output = clf.predict(text_transformed.toarray())
    
    out = clf.predict(vect.transform(text_df["message"]))
    print(out)
    if out[0] == 0: 
        class_label = 'ham i.e not spam'
        return render_template('results.html', classification=class_label) 
    else:
        class_label = 'spam'
        return render_template('results.html', classification=class_label) 

#@app.route('/authorize')
#def authorize():
@app.route('/email_results')
def show_results():
    from gmail import get_emails
    df = get_emails.get_emails()
    spam = df.loc[df.class_label=='spam']
    ham = df.loc[df.class_label=='ham']
    return render_template('view_email_results.html',
        tables=[spam.to_html(classes='spam'), ham.to_html(classes='ham')],
    titles = ['na', 'Spam Email', 'Ham Email'] )



if __name__ == "__main__":
    app.run(debug=True)