from http import HTTPStatus

from basic_deploy.app import Role, User, db


def test_get_user_success(client):
    # Given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()
    user = User(username="john", password="1234", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    # When
    response = client.get(f"/users/{user.id}")

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": user.id,
        "username": user.username,
    }


def test_get_user_not_found(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user_id = 1

    response = client.get(f"/users/{user_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_list_user(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="John", password="1234", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login",
        json={"username": user.username, "password": user.password},
    )
    access_token = response.json["access_token"]

    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.json == {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "role": {
                    "id": user.role.id,
                    "name": user.role.name,
                },
            }
        ]
    }


def test_create_user(client, access_token):
    role_id = db.session.execute(
        db.select(Role.id).where(Role.name == "admin")
    ).scalar()
    payload = {"username": "Jose", "password": "1234", "role_id": role_id}

    response = client.post(
        "/users/",
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.json == {"message": "user created!"}
