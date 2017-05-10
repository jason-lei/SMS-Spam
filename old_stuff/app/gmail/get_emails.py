from __future__ import print_function
import numpy as np
import pandas as pd
import pickle

import httplib2
import os

from gmail_functions import *
from apiclient import discovery, errors
from oauth2client import client, tools
from oauth2client.file import Storage
import base64
import email

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/data-science-web-client.json
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'

CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'data-science-web-client'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
       os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'data-science-web-client.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
             credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
             credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

    
def get_emails():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    # ***** print out user email labels *****

    # if not labels:
    #     print('No labels found.')
    # else:
    #   print('Labels:')
    #   for label in labels:
    #     print(label['name'])
    

    # ***** adding a label to the mailbox *****
    #label = MakeLabel("mojdeh")
    #crtLabel = CreateLabel(service, 'me', label)

    # ***** getting all email id's from user's inbox *****
    messages = ListMessagesMatchingQuery(service, 'me') 
    df = pd.DataFrame(data = None, columns=['message'])
    print( "There are %d many messages in your inbox." % len(messages) )
    for i in range(50): #get first 50 emails
        df.loc[i] = GetMessage(service, 'me', messages[i]['id']) ['snippet']

    # classify emails 
    clf  = pickle.load(open(
        "/Users/andressoto/spring/data-science-industry/SMS-Spam/model/classifier.pkl", "rb"))
    vect = pickle.load(
        open("/Users/andressoto/spring/data-science-industry/SMS-Spam/model/vectorizer.pkl", "rb"))
    df["class_num"] = clf.predict( vect.transform(df["message"]) )
    df["class_label"] = df["class_num"].map({0:'ham', 1:"spam"})
    #df.to_csv("my_email_classification.csv", encoding='utf-8')s
    return df

def main():
    get_emails()
if __name__ == '__main__':
    main()
