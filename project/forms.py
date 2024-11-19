from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")


class CreateArticle(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    tags = StringField("Tags", validators=[DataRequired()])
    submit = SubmitField("Create Article")


class EditArticle(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    date = StringField("Date", validators=[DataRequired()])
    tags = StringField("Tags", validators=[DataRequired()])
    submit = SubmitField("Edit Article")
    