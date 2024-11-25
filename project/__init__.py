"""
This has to be executed every time in new terminal for app to be able to run
Otherwise it will not work
export FLASK_APP=project
export FLASK_ENV=development  # Optional: Enables debug mode
"""

from flask import Flask
from .extension import db, login_manager
from .models import User
from .blueprints.main import main
from .blueprints.admin import admin


def create_app(database_uri="sqlite:///db.sqlite"):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "supersecretkey"
    app.app_context().push()


    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == user_id).first()

    app.register_blueprint(main)
    app.register_blueprint(admin)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)