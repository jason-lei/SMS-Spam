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
    from flask import Flask, jsonify
    from sklearn.externals import joblib
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.feature_selection import SelectPercentile, f_classif
    import pandas as pd
    d = {'v2': ("%s" %_text)}
    text_df = pd.DataFrame(data=d, index={0})
    vocabulary_to_load =joblib.load('vectorizer.pkl')
    vectorizer2 = TfidfVectorizer(vocabulary=vocabulary_to_load)
    vectorizer2.fit(vocabulary_to_load)
    text_transformed = vectorizer2.transform(text_df)
    _output = clf.predict(text_transformed.toarray())
    print(_output)

    return render_template('results.html', classification=_output) 

if __name__ == "__main__":
	from sklearn.externals import joblib
	clf = joblib.load('model.pkl')
	app.run(debug=True)
    # app.run(port=8080)