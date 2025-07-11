from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    nickname: Mapped[str] = mapped_column(String(25), nullable=False)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="usuario", cascade="all, delete-orphan")
    comentarios: Mapped[list["Comment"]] = relationship("Comment", back_populates="usuario", cascade="all, delete-orphan")
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="usuario", cascade="all, delete-orphan")
    notificaciones_enviadas: Mapped[list["Notification"]] = relationship("Notification", back_populates="emisor", foreign_keys="[Notification.emisor_id]")
    notificaciones_recibidas: Mapped[list["Notification"]] = relationship("Notification", back_populates="receptor", foreign_keys="[Notification.receptor_id]")
    siguiendo: Mapped[list["Follower"]] = relationship("Follower", back_populates="follower", foreign_keys="[Follower.follower_id]")
    seguidores: Mapped[list["Follower"]] = relationship("Follower", back_populates="followed", foreign_keys="[Follower.followed_id]")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nickname": self.nickname
        }

class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    post_url: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    usuario: Mapped["User"] = relationship("User", back_populates="posts")
    comentarios: Mapped[list["Comment"]] = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="post", cascade="all, delete-orphan")
    notificaciones: Mapped[list["Notification"]] = relationship("Notification", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "post_url": self.post_url,
            "user_id": self.user_id
        }

class Like(db.Model):
    __tablename__ = "like"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    usuario: Mapped["User"] = relationship("User", back_populates="likes")
    post: Mapped["Post"] = relationship("Post", back_populates="likes")

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id
        }

class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    content: Mapped[str] = mapped_column(String(500), nullable=False)

    usuario: Mapped["User"] = relationship("User", back_populates="comentarios")
    post: Mapped["Post"] = relationship("Post", back_populates="comentarios")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "content": self.content
        }

class Follower(db.Model):
    __tablename__ = "follower"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    followed_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    follower: Mapped["User"] = relationship("User", foreign_keys=[follower_id], back_populates="siguiendo")
    followed: Mapped["User"] = relationship("User", foreign_keys=[followed_id], back_populates="seguidores")

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "followed_id": self.followed_id
        }

class Notification(db.Model):
    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    emisor_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    receptor_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=True)
    message: Mapped[str] = mapped_column(String(250), nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    emisor: Mapped["User"] = relationship("User", foreign_keys=[emisor_id], back_populates="notificaciones_enviadas")
    receptor: Mapped["User"] = relationship("User", foreign_keys=[receptor_id], back_populates="notificaciones_recibidas")
    post: Mapped["Post"] = relationship("Post", back_populates="notificaciones")

    def serialize(self):
        return {
            "id": self.id,
            "emisor_id": self.emisor_id,
            "receptor_id": self.receptor_id,
            "type": self.type,
            "post_id": self.post_id,
            "message": self.message,
            "is_read": self.is_read
        }
