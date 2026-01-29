import pytest
from app import Role, User, create_app, db


@pytest.fixture
def app():
    app = create_app(
        {
            "SECRET_KEY": "test",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///",
            "JWT_SECRET_KEY": "test",
        }
    )
    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def access_token(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="Joel", password="1234", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login",
        json={"username": user.username, "password": user.password},
    )
    return response.json["access_token"]
