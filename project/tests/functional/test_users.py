import json
import pytest
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
    assert "added" in data["message"]


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
    assert "michael" in data[1]["username"]
    assert "michael@mherman.org" in data[1]["email"]
    assert "fletcher" in data[0]["username"]
    assert "fletcher@notreal.com" in data[0]["email"]


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
    assert f"{user.email} was removed" in data["message"]

    resp_3 = client.get("/users")
    data = json.loads(resp_3.data.decode())
    assert resp_3.status_code == 200
    assert len(data) == 0


def test_cannot_delete_user_if_id_is_wrong(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    add_user("remove", "remove@gmail.com")
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 1

    resp_2 = client.delete(f"/users/99999")
    data = json.loads(resp_2.data.decode())

    assert resp_2.status_code == 404
    assert "User 99999 does not exist" in data["message"]

    resp_3 = client.get("/users")
    data = json.loads(resp_3.data.decode())
    assert resp_3.status_code == 200
    assert len(data) == 1


def test_cannot_delete_user_if_id_is_missing(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    add_user("remove", "remove@gmail.com")
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


# Positive
def test_can_update_user(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    user = add_user("counter1", "counter1@gmail.com")
    client = test_app.test_client()
    resp_1 = client.get("/users")
    data = json.loads(resp_1.data.decode())
    assert resp_1.status_code == 200
    assert len(data) == 1
    assert "counter1" in data[0]["username"]
    assert "counter1@gmail.com" in data[0]["email"]

    resp_one = client.put(
        f"/users/{user.id}",
        data=json.dumps({"username": "counter2", "email": "counter2@gmail.com"}),
        content_type="application/json",
    )

    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert f"{user.id} was updated" in data["message"]

    resp_two = client.get(f"users/{user.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "counter2" in data["username"]
    assert "counter2@gmail.com" in data["email"]

    resp_three = client.get("/users")
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data) == 1


# Negative
@pytest.mark.parametrize(
    "user_id, payload, status_code, message",
    [
        [1, {}, 400, "Input payload validation failed"],
        [1, {"email": "invalid@gmail.com"}, 400, "Input payload validation failed"],
        [1, {"username": "invalid"}, 400, "Input payload validation failed"],
        [
            999,
            {"username": "invalid", "email": "invalid@gmail.com"},
            404,
            "User 999 does not exist",
        ],
    ],
)
def test_cannot_update_invalid_user(
    test_app, test_database, user_id, payload, status_code, message
):
    client = test_app.test_client()
    resp = client.put(
        f"/users/{user_id}", data=json.dumps(payload), content_type="application/json"
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]
