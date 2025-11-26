from os.path import defpath

from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event
from slugify import slugify
import os
import shutil
from flask import current_app


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    square = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(15), nullable=False)
    price_base = db.Column(db.Integer, nullable=False)
    price_with_communications = db.Column(db.Integer)
    price_ready = db.Column(db.Integer)
    mortgage_price_per_month = db.Column(db.Integer)

    images_directory_path = db.Column(db.String(300), nullable=False)

    images = db.relationship(
        "ProjectImages",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Project {self.id} {self.title}>"


# ─────────────────────────────────────────────────────────────
# BEFORE INSERT
# ─────────────────────────────────────────────────────────────

@event.listens_for(Project, "before_insert")
def project_before_insert(mapper, connection, target):
    # генерируем slug
    target.slug = slugify(target.title)

    # путь до папки
    directory = target.slug
    target.images_directory_path = os.path.join(
        current_app.static_folder,
        'uploads',
        directory
    )

    # создаём папку
    try:
        os.makedirs(target.images_directory_path, exist_ok=True)
    except OSError as e:
        print(f"[ERROR] Cannot create directory {target.images_directory_path}: {e}")


# ─────────────────────────────────────────────────────────────
# BEFORE UPDATE
# ─────────────────────────────────────────────────────────────

@event.listens_for(Project, "before_update")
def project_before_update(mapper, connection, target):
    state = db.inspect(target)

    # проверяем, изменился ли title
    if not state.attrs.title.history.has_changes():
        return

    old_directory = target.images_directory_path

    # генерируем новый slug
    new_slug = slugify(target.title)
    target.slug = new_slug

    new_directory = os.path.join(
        current_app.static_folder,
        'uploads',
        new_slug
    )

    # пытаемся переименовать папку
    try:
        if os.path.exists(old_directory):
            os.rename(old_directory, new_directory)
            print(f"[OK] Directory renamed: {old_directory} → {new_directory}")
    except OSError as e:
        print(f"[ERROR] Fail rename {old_directory} → {new_directory}: {e}")

    # обновляем путь в базе
    target.images_directory_path = new_directory


# ─────────────────────────────────────────────────────────────
# AFTER DELETE
# ─────────────────────────────────────────────────────────────

@event.listens_for(Project, "after_delete")
def project_after_delete(mapper, connection, target):
    try:
        if os.path.exists(target.images_directory_path):
            shutil.rmtree(target.images_directory_path)
            print(f"[OK] Directory deleted: {target.images_directory_path}")
    except OSError as e:
        print(f"[ERROR] Cannot delete directory {target.images_directory_path}: {e}")


# ─────────────────────────────────────────────────────────────

class ProjectImages(db.Model):
    __tablename__ = "project_images"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)

    project_id = db.Column(
        db.Integer,
        db.ForeignKey(Project.id, ondelete="CASCADE"),
        nullable=False,
    )

    project = db.relationship("Project", back_populates="images")

    @property
    def url(self):
        return os.path.join('uploads', self.project.slug, self.filename)

    @property
    def full_path(self):
        return os.path.join(self.project.images_directory_path, self.filename)

    def __repr__(self):
        return f"<ProjectImage {self.id} {self.filename}>"
