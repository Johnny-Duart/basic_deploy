from flask import Blueprint, request

from basic_deploy.models.models import Post, db

app = Blueprint("post", __name__, url_prefix="/posts")


def create_post():
    data = request.json
    post = Post(
        title=data["title"], body=data["body"], author_id=data["author_id"]
    )
    db.session.add(post)
    db.session.commit()


def select_post():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()

    return [
        {
            "title": post.title,
            "body": post.body,
            "user": {
                "id": post.user.id,
                "username": post.user.username,
            },
        }
        for post in posts
    ]


@app.route("/", methods=["GET", "POST"])
def list_or_create_post():
    if request.method == "POST":
        create_post()
        return {"message": "post created!"}
    else:
        pass
    return {"posts:": select_post()}
