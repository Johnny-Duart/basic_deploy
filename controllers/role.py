from http import HTTPStatus

from flask import Blueprint, request

from ..app import Role, db

app = Blueprint("role", __name__, url_prefix="/roles")


@app.route("/", methods=["POST"])
def create_role():
    data = request.json
    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()
    return {"message": "role created!"}, HTTPStatus.CREATED


def list_role():
    query = db.select(Role)
    roles = db.session.execute(query).scalars()

    return [
        {
            "name": role.name,
        }
        for role in roles
    ]


@app.route("/", methods=["GET"])
def list_roles():
    return {"roles:": list_role()}
