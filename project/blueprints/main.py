from flask import Blueprint, render_template
from project.models import Articles


main = Blueprint("main", __name__)


@main.route("/")
def index():
    articles = Articles.query.all()

    return render_template("index.html", articles=articles)


@main.route("/article/<article_id>")
def article(article_id):
    article = Articles.query.filter(Articles.id == article_id).first()
    
    return render_template("article.html", article=article)