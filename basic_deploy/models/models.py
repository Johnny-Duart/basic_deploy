from datetime import datetime

import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")


class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        sa.String, unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates="user")
    post: Mapped["Post"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}), username={self.username!r}"


class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[datetime] = mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )
    author_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    user: Mapped[list["User"]] = relationship(back_populates="post")

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}), title={self.title!r}, author_id={self.author_id}"
