from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, \
    TextAreaField, validators
from wtforms import widgets, Form
from wtforms.validators import DataRequired, Regexp
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.fields import simple, core


class LoginForm(FlaskForm):
    name = simple.StringField(
        'Username',
        validators=[
            validators.DataRequired('Please fill in the username'),
            # validators.Length(min=3, max=10, message='Incorrect username!')
        ],
        # widget=widgets.TextInput(),
        render_kw={
            'for': 'username1',
            'class': 'input-sign',
            'placeholder': 'USERNAME'}
    )
    pwd = simple.PasswordField(
        'Password',
        validators=[
            validators.DataRequired('Please fill in the password'),
            # validators.Length(min=6, max=15, message='Password not match the username')
        ],
        # widget=widgets.TextInput(),
        render_kw={
            'for': 'password1',
            'class': 'input-sign',
            'placeholder': 'PASSWORD'}
    )
    submit = SubmitField('Confirm',
                          render_kw={'class': 'buttonSubmit'}
                         )


class UpdateForm(FlaskForm):
    # movie_pic = FileField('M_pic', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only pictures please')])
    movie_name = StringField('M_name', validators=[DataRequired()])
    movie_time = DateField('Email')
    intro = TextAreaField('Introduction', validators=[DataRequired()])
    address = StringField('Address')
    phone_num = StringField('Phone number')
    name = StringField('Name')
    submit = SubmitField('Submit')


class ReviewForm(FlaskForm):
    title = StringField('TITLE', validators=[DataRequired()])
    text = TextAreaField('YOUR COMMENT ...', validators=[DataRequired()])
    send = SubmitField('SEND')
