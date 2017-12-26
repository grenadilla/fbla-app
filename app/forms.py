from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import Required
from app import db, models


class NewUser(FlaskForm):
    usertype = SelectField("Student or Teacher?", choices=[('student', 'Student'), ('teacher', 'Teacher')], validators=[Required()])
    name = StringField("Name of user", validators=[Required()])
    submit = SubmitField('Submit')

class NewAuthor(FlaskForm):
    name = StringField("Name of author", validators=[Required()])
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
    usertype = SelectField("Student or Teacher?", choices=[('student', 'Student'), ('teacher', 'Teacher')], validators=[Required()])
    submit = SubmitField('Submit')


class EditBook(FlaskForm):
    title = StringField("New name", default="", validators=[Required()])
    author = SelectField("New author", choices=[], validators=[Required()])
    submit = SubmitField('Submit')


class EditUserType(FlaskForm):
    student_borrow_length = IntegerField("Student borrow length (days)", validators=[Required()])
    student_fine = IntegerField("Student fine (cents)", validators=[Required()])
    student_book_limit = IntegerField("Student book limit", validators=[Required()])
    teacher_borrow_length = IntegerField("Teacher borrow length (days)", validators=[Required()])
    teacher_fine = IntegerField("Teacher fine (cents)", validators=[Required()])
    teacher_book_limit = IntegerField("Teacher book limit", validators=[Required()])
    submit = SubmitField('Submit')
