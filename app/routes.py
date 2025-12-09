import os.path
import io, os

from flask import Blueprint, render_template, redirect, current_app, request, jsonify, flash, send_file, abort
from flask import jsonify
from flask_mail import Message

from PIL import Image

from app.models import Project, ProjectImages
from app import mail

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    projects = Project.query.all()
    bg_image_url = projects[0].images.first().url
    return render_template('index.html', projects=projects)


@main_bp.route('/img_compressed/<path:filename>')
def img_compressed(filename):
    full_path = os.path.join(current_app.static_folder, filename)

    if not os.path.exists(full_path):
        abort(404)

    img = Image.open(full_path)

    # Буфер в памяти
    buffer = io.BytesIO()

    # Сжатие на ~50% (quality 50–60 отлично)
    img.save(buffer, format="WEBP", quality=10, method=6)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/webp",
        as_attachment=False,
        download_name="compressed.webp"
    )


@main_bp.route('/img_blur/<path:filename>')
def img_blur(filename):
    full_path = os.path.join(current_app.static_folder, filename)

    if not os.path.exists(full_path):
        abort(404)

    img = Image.open(full_path)
    img.thumbnail((50, 50))

    # 2. Сохраняем в памяти
    buffer = io.BytesIO()
    img.save(
        buffer,
        format="WEBP",
        quality=20,
        method=6
    )
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/webp",
        download_name="blur.webp"
    )


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
