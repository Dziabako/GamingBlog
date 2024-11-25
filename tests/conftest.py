### PYTEST SETUP ENVIRENMENT ###
# All paths in the main project for imports have to be absolute (.extension) #
import pytest
from project import create_app, db


@pytest.fixture()
def app():
    # Creating database in memory for testing which is destroyed after testing is finished
    app = create_app("sqlite://")
    app.config['TESTING'] = True
    # Disable CSRF protection for testing
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()

    print("CREATING DATABASE")
    # Returning the app 
    yield app
        

@pytest.fixture()
def client(app):
    # Simulating requests to the app
    return app.test_client()
