# #!/usr/bin/env python

from __future__ import print_function # In python 2.7
import sys
from flask import Flask, render_template, json, request, redirect
from flask_wtf import Form

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

if __name__ == "__main__":
	from sklearn.externals import joblib
	from sklearn.feature_extraction.text import TfidfVectorizer
	from sklearn.feature_selection import SelectPercentile, f_classif
	clf = joblib.load('stored_pickles/model.pkl')
	selector = joblib.load('stored_pickles/selector.pkl')
	vocabulary_to_load =joblib.load('stored_pickles/vectorizer.pkl')
	vectorizer = TfidfVectorizer(vocabulary=vocabulary_to_load)
	vectorizer.fit(vocabulary_to_load)
	app.run(debug=True)
    # app.run(port=8080)