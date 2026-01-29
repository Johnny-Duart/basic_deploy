import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from basic_deploy.models.models import db

migrate = Migrate()
jwt = JWTManager()


def create_app(test_config=None):
    app = Flask(
        __name__,
        instance_path=os.path.join(os.path.dirname(__file__), "instance"),
        instance_relative_config=False,
    )

    database_url = os.environ.get("DATABASE_URL")

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=database_url
        or "sqlite:///" + os.path.join(app.instance_path, "dio_bank.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    from basic_deploy.controllers import auth, post, role, user

    app.register_blueprint(post.app)
    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
    app.run()
