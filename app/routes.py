import os.path
from pathlib import Path
import shutil

from flask import Blueprint, render_template, redirect, current_app, request, jsonify, flash
from flask_login import login_required, current_user
from flask_wtf.csrf import CSRFError
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from slugify import slugify
from app import db
from app.models import Project, ProjectImages
from app.forms import ProjectForm

from flask_mail import Message
from app import mail

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)


@main_bp.route('/details/<slug>')
def details(slug):
    # project = Project.query.get(id)
    project = Project.query.filter_by(slug=slug).first_or_404()
    first_image_url = os.path.join(current_app.static_folder, project.images.first().url)

    projects = Project.query.all()
    return render_template('project_details.html', project=project, first_image_url=first_image_url, projects=projects)


@main_bp.route("/send", methods=["POST"])
def send():
    try:
        name = request.form.get("name")
        phone = request.form.get("phone")
        message_text = request.form.get("message")

        msg = Message(
            "Новая заявка с сайта",
            recipients=["kf@iralim.com"]
        )

        msg.body = f"""
Имя: {name}
Телефон: {phone}
Сообщение:
{message_text}
        """

        mail.send(msg)

        return jsonify(status="ok")

    except Exception as e:
        return jsonify(status="error", error=str(e))


@main_bp.route('/check_title')
def check_title():
    title = request.args.get('title', '').strip()
    exists = Project.query.filter_by(title=title).first() is not None
    return jsonify({'exists': exists})


# TEST
@main_bp.route('/test')
def test():
    project = Project.query.first()
    projects = Project.query.all()
    return render_template('____test.html', project=project, projects=projects)
