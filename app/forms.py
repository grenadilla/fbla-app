from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import Required
from app import db, models


class NewData(FlaskForm):
    type = SelectField("Student, Teacher, or Author?", choices=[('student', 'Student'), ('teacher', 'Teacher'), ('author', 'Author')], validators=[Required()])
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


class EditUser(FlaskForm):
    name = StringField("New name", default="", validators=[Required()])
    submit = SubmitField('Submit')


class EditBook(FlaskForm):
    title = StringField("New name", default="", validators=[Required()])
    author = SelectField("New author", choices=[], validators=[Required()])
    submit = SubmitField('Submit')
