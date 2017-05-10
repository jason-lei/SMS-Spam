Andres Soto and Jason Lei

## Project Description
insert it here


static/
	contains all .css files 

templates/
	contains all .html files

old_stuff/ 
	contains all previous files that led up to the final end-product

stored_pickles/
	contains relevant pickle files for classifier used in app


make-model.py: creates the model and stores pickle files into stored_pickles/ using data from spam.csv

spam.csv: raw dataset obtained from kaggle

client_secrets.json: contains relevant and necessary information for access to gmail API 

gmail_functions.py: contains functions created that use gmail API s

app.py: main server .py file (run this using python3 in the command line for local server startup)


