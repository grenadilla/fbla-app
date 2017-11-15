from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required
from app import db, models


class NewData(FlaskForm):
    type = SelectField("User or Author?", choices=[('user', 'User'), ('author', 'Author')], validators=[Required()])
    name = StringField("Name of user or author", validators=[Required()])
    submit = SubmitField('Submit')


class NewBook(FlaskForm):
    title = StringField("Title of Book", validators=[Required()])
    choices = []
    authors = models.Author.query.all()
    for author in authors:
        choices.append((str(author.id), author.name))

    author = SelectField("Author of Book", choices=choices, validators=[Required()])
    submit = SubmitField('Submit')


class Login(FlaskForm):
    login_data = StringField("User of ID or name", validators=[Required()])
    submit = SubmitField('Login')


class DeleteData(FlaskForm):
    submit = SubmitField('DELETE ALL DATA')
