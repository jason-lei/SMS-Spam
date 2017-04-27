from __future__ import print_function
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as pyplot
import seaborn as sns 


from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, classification_report


sms = pd.read_csv("../data/spam.csv", usecols=[0, 1], 
	header=0, names=['class_label', 'message'], encoding='latin-1')

x = sms.class_label.value_counts()

print("There are %d ham entries."  % x[0])
print("There are %d spam entries."  % x[1])


sms['class_number'] = sms['class_label'].map({'ham':0, 'spam':1})
sms = sms[['message', 'class_label', 'class_number']]

X = sms['message']
y = sms['class_number']
X_train, X_test, y_train, y_test = train_test_split(X, y, 
	train_size=.8, random_state=42)

# create CountVectorizer Instance 
vect = CountVectorizer()

vect.fit(X_train)
X_train_df = vect.transform(X_train)
X_test_df = vect.transform(X_test)

# dictionary, that will hold accuracy results 
# of different classificationmodels

prediction = {}
clf = MultinomialNB()
clf.fit(X_train_df,y_train)
prediction['Multinomial'] = clf.predict(X_test_df)
#print(clf.score(X_test_df, y_test)
pickle.dump(clf, open("classifier.pkl", "wb"))
pickle.dump(vect, open("vectorizer.pkl", "wb"))



