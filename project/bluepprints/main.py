from flask import Blueprint, render_template
from models import Articles


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/article/<article_id>")
def article(article_id):
    article = Articles.query.get(article_id)
    return render_template("article.html", article=article)