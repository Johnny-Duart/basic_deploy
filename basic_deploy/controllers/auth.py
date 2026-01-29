from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from basic_deploy.models.models import User, db

app = Blueprint("auth", __name__, url_prefix="/auth")


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    user = db.session.execute(
        db.select(User).where(User.username == username)
    ).scalar()
    if not user or user.password != password:
        return {"msg": "Nao deu p acessar legal nao"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}
