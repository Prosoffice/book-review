from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField
from wtforms.validators import InputRequired


class RegForm(FlaskForm):
    full_name = StringField("Full Name", validators=[InputRequired()], render_kw={'placeholder':'Frank Lewis'})
    email = StringField('Email', render_kw={'placeholder':'franklewis@gmail.com'}, validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', render_kw={'placeholder': 'franklewis@gmail.com'}, validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])


class SearchForm(FlaskForm):
    search = StringField(render_kw={'placeholder':'Search for books'},  validators=[InputRequired()])


class ReviewForm(FlaskForm):
    rating = IntegerField("Rating", validators=[InputRequired()])
    feedback = TextAreaField("What do you think of this book?", validators=[InputRequired()])