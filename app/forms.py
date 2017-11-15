from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required

class NewData(FlaskForm):
    type = SelectField("User, Book, or Author?", choices=[('user', 'User'), ('book', 'Book'), ('author', 'Author')], validators=[Required()])
    name = StringField("Name of user, book, or author", validators=[Required()])
    submit = SubmitField('Submit')

class Login(FlaskForm):
    login_data = StringField("User of ID or name", validators=[Required()])
    submit = SubmitField('Login')

class DeleteData(FlaskForm):
    submit = SubmitField('DELETE ALL DATA')
