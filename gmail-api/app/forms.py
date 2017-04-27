from flask_wtf import Form 
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

# import the Form class and two form field classes

class LoginForm(Form):
	openid = StringField('openid', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)