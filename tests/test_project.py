def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<h1>Gaming Blog</h1>" in response.data