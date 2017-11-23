from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import Required
from app import db, models


class NewData(FlaskForm):
    type = SelectField("User or Author?", choices=[('user', 'User'), ('author', 'Author')], validators=[Required()])
    name = StringField("Name of user or author", validators=[Required()])
    submit = SubmitField('Submit')


class NewBook(FlaskForm):
    title = StringField("Title of Book", validators=[Required()])
    author = SelectField("Author of Book", choices=[], validators=[Required()])
    copies = IntegerField("Number of Copies", default=1, validators=[Required()])
    submit = SubmitField('Submit')


class Login(FlaskForm):
    login_data = StringField("User of ID or name", validators=[Required()])
    submit = SubmitField('Login')


class DeleteData(FlaskForm):
    submit = SubmitField('DELETE ALL DATA')
