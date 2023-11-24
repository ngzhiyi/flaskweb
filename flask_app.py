
# A very simple Flask Hello World app for you to get started with...

from forms import CommentDeletionForm, LoginForm, CommentForm
from sqlalchemy import func
from datetime import datetime, timezone, timedelta
from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import check_password_hash
from flask_login import current_user, login_required, logout_user, login_user, LoginManager, UserMixin
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)

csrf = CSRFProtect(app)

app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    hostname=os.getenv("DB_HOSTNAME"),
    databasename=os.getenv("DB_NAME"),
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

# create a timezone object for GMT+8
gmt8_timezone = timezone(timedelta(hours=8))

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, server_default=func.now(), default=datetime.now)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
@csrf.exempt
def delete_comment(comment_id):
    # Get the comment by its ID
    comment = Comment.query.get(comment_id)

    ## if comment and current_user.id == comment.commenter_id:
    if current_user.is_authenticated and (current_user.username == 'admin' or current_user.id == comment.commenter_id):
        # Use the delete_comment method to delete the comment
        comment.delete_comment()

    return redirect(url_for('index'))  # Redirect to the main page after deletion

@app.route("/", methods=["GET", "POST"])
def index():
    comment_deletion_form = CommentDeletionForm()
    comment_form = CommentForm()

    if request.method == "POST":
        # Check if the comment form for posting comments is submitted and valid
        if comment_form.validate_on_submit():
            if current_user.is_authenticated:
                comment_content = comment_form.contents.data
                comment = Comment(content=comment_content, commenter=current_user)
                db.session.add(comment)
                db.session.commit()
                # Redirect after posting the comment if needed
                return redirect(url_for('index'))

        # Check if the comment deletion form is submitted and valid
        elif comment_deletion_form.validate_on_submit():
            comment_id_to_delete = comment_deletion_form.comment_id.data
            delete_comment(comment_id_to_delete)
            # Redirect after deleting the comment if needed
            return redirect(url_for('index'))

    comments = Comment.query.all()

    return render_template("main_page.html", comments=comments, gmt8_timezone=gmt8_timezone, timezone=timezone, comment_deletion_form=comment_deletion_form, comment_form=comment_form)

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = load_user(form.username.data)

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')

    return render_template("login_page.html", form=form)

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
