from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
  username = StringField('Username',
                          validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField('Email',
                          validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
  username = StringField('Username',
                          validators=[DataRequired(), Length(min=2, max=20)])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Sign Up')

class TransferForm(FlaskForm):
    VALID_CURRENCIES = [('USD', 'USD')]

    to = SelectField(u'To', choices=[], validators=[DataRequired()])
    currency = SelectField(u'Currency', choices=VALID_CURRENCIES, validators=[DataRequired()])
    network = SelectField(u'Type', choices=[('ACH-US', 'ACH-US')], validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired('num required.')])
    pay = SubmitField('Pay')


