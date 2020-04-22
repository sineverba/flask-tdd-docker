import json
from project.api.models import User


# Positive test
def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps(
            {"username": "username_of_example", "email": "info@example.com"}
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "success" in data["message"]


# Negative test
def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post("/users", data=json.dumps({}), content_type="application/json")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


# Positive test
def test_get_single_user(test_app, test_database, add_user):
    user = add_user("gogogo", "info@example.com")

    client = test_app.test_client()
    resp = client.get(f"/users/{user.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "gogogo" in data["username"]
    assert "info@example.com" in data["email"]


def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_all_users(test_app, test_database, add_user):
    test_database.session.query(User).delete()  # new
    add_user("michael", "michael@mherman.org")
    add_user("fletcher", "fletcher@notreal.com")
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert "michael" in data[0]["username"]
    assert "michael@mherman.org" in data[0]["email"]
    assert "fletcher" in data[1]["username"]
    assert "fletcher@notreal.com" in data[1]["email"]

# Positive
def test_delete_user(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    user = add_user("remove", "remove@gmail.com")
    client = test_app.test_client()
    resp_1 = client.get("/users")
    data = json.loads(resp_1.data.decode())
    assert resp_1.status_code == 200
    assert len(data) == 1

    resp_2 = client.delete(f"/users/{user.id}")
    data = json.loads(resp_2.data.decode())

    assert resp_2.status_code == 200
    assert f"{user.id} removed" in data['message']

    resp_3 = client.get("/users")
    data = json.loads(resp_3.data.decode())
    assert resp_3.status_code == 200
    assert len(data) == 0


def test_cannot_delete_user_if_id_is_wrong(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    user = add_user("remove", "remove@gmail.com")
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 1

    resp_2 = client.delete(f"/users/99999")
    data = json.loads(resp_2.data.decode())

    assert resp_2.status_code == 404
    assert "ID 99999 not found" in data['message']

    resp_3 = client.get("/users")
    data = json.loads(resp_3.data.decode())
    assert resp_3.status_code == 200
    assert len(data) == 1


def test_cannot_delete_user_if_id_is_missing(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    user = add_user("remove", "remove@gmail.com")
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 1

    resp_2 = client.delete("/users")
    data = json.loads(resp_2.data.decode())

    assert resp_2.status_code == 405

    resp_3 = client.get("/users")
    data = json.loads(resp_3.data.decode())
    assert resp_3.status_code == 200
    assert len(data) == 1
