from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extension import db
from models import User
from forms import LoginForm, RegisterForm


admin = Blueprint("admin", __name__)


@admin.route("/register")
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter(User.username == username).first()

        if user:
            flash("Username is already taken!")
            return redirect(url_for("admin.login"))
        else:
            new_user = User(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()

            flash("You are registered!")
            return redirect(url_for("admin.login"))
    
    return render_template("register.html", form=form)


@login_required
@admin.route("/login")
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter(User.username == username).first()

        if not user:
            flash("There is not such user! Register First!")
            return redirect(url_for("admin.register"))
        elif not check_password_hash(user.password, password):
            flash("Password is incorrect!")
            return redirect(url_for("admin.login"))
        else:
            login_user(user)
            flash("You are logged in!")
            return redirect(url_for("main.index"))


    return render_template("login.html", form=form)


@login_required
@admin.route("/logout")
def logout():
    logout_user()
    flash("You are logged out!")
    return redirect(url_for("main.index"))


@admin.route("/create_article")
def create_article():
    pass


@admin.route("/edit_article/<article_id>")
def edit_article(article_id):
    pass


@admin.route("/delete_article/<article_id>")
def delete_article(article_id):
    pass
