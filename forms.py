# forms.py

from flask_wtf import FlaskForm
from wtforms.fields import HiddenField, SubmitField, TextAreaField
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class CommentDeletionForm(FlaskForm):
    comment_id = HiddenField()
    csrf_token = HiddenField()
    submit = SubmitField("Delete Comment")
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class CommentForm(FlaskForm):
    csrf_token = HiddenField()
    contents = TextAreaField("Comment", validators=[DataRequired()])  # Add this line for the contents field
    submit = SubmitField("Post Comment")
