from datetime import datetime
from project.models import User, Articles


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<h1>Gaming Blog</h1>" in response.data


def test_login(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"<h2>Login</h2>" in response.data


def test_register(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"<h2>Register</h2>" in response.data


def test_create_article_redirect(client):
    response = client.get("/create_article", follow_redirects=True)
    assert response.status_code == 200
    assert b"<h2>Login</h2>" in response.data


# App is added to use app context for seaching database
def test_new_user_register(client, app):
    response = client.post("/register", data={"username": "test", "password": "test", "confirm_password": "test"}, follow_redirects=True)

    with app.app_context():
        user = User.query.filter_by(username="test").first()
        assert user is not None
        assert user.username == "test"


def test_new_user_login(client, app):
    response = client.post("/register", data={"username": "test", "password": "test", "confirm_password": "test"}, follow_redirects=True)
    response = client.post("/login", data={"username": "test", "password": "test"}, follow_redirects=True)

    assert response.status_code == 200
    assert b"Logout" in response.data


def test_new_user_logout(client):
    response = client.post("/register", data={"username": "test", "password": "test", "confirm_password": "test"}, follow_redirects=True)
    response = client.post("/login", data={"username": "test", "password": "test"}, follow_redirects=True)
    response = client.get("/logout", follow_redirects=True)

    assert response.status_code == 200
    assert b"Logout" not in response.data


def test_create_new_article(client):
    client.post("/register", data={"username": "test", "password": "test", "confirm_password": "test"}, follow_redirects=True)
    client.post("/login", data={"username": "test", "password": "test"}, follow_redirects=True)

    response = client.post("/create_article", data={"title": "tested article", "content": "test", "author": "test", "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "tags": "test"}, follow_redirects=True)

    assert response.status_code == 200
    assert b"tested article" in response.data


def test_edit_article(client):
    client.post("/register", data={"username": "test", "password": "test", "confirm_password": "test"}, follow_redirects=True)
    client.post("/login", data={"username": "test", "password": "test"}, follow_redirects=True)

    client.post("/create_article", data={"title": "tested article", "content": "test", "author": "test", "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "tags": "test"}, follow_redirects=True)

    response = client.post("/create_article", data={"title": "edited article", "content": "test", "author": "test", "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "tags": "test"}, follow_redirects=True)

    assert response.status_code == 200
    assert b"edited article" in response.data


def test_delete_article(client, app):
    client.post("/register", data={"username": "test", "password": "test", "confirm_password": "test"}, follow_redirects=True)
    client.post("/login", data={"username": "test", "password": "test"}, follow_redirects=True)

    response = client.post("/create_article", data={
        "title": "article to delete",
        "content": "test",
        "author": "test",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tags": "test"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"article to delete" in response.data

    with app.app_context():
        article = Articles.query.filter_by(title="article to delete").first()
        assert article is not None, f"Article was not created: {article}"
        print(f"Article created: {article}")

    response = client.post(f"/delete_article/{article.id}", follow_redirects=True)
    assert response.status_code == 200
    assert b"article to delete" not in response.data

    with app.app_context():
        article = Articles.query.filter_by(title="article to delete").first()
        assert article is None, f"Article was not deleted: {article}"
        print(f"Article after deletion: {article}")