import os.path
import io, os

from flask import Blueprint, render_template, redirect, current_app, request, jsonify, flash, send_file, abort, url_for
from flask import jsonify
from flask_mail import Message
from app import mail
from PIL import Image, ImageFilter

from app.models import Project, ProjectImages

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    projects = Project.query.all()
    img_url = ensure_hero_webp(os.path.join(current_app.static_folder, 'images', 'piclumen4.png', ), overwrite=False)
    return render_template('index.html', projects=projects, hero_bg=img_url)


@main_bp.route('/details/<slug>')
def details(slug):
    # project = Project.query.get(id)
    project = Project.query.filter_by(slug=slug).first_or_404()
    first_image_url = os.path.join(current_app.static_folder, project.images.first().url)

    projects = Project.query.all()
    return render_template('project_details.html', project=project, first_image_url=first_image_url, projects=projects)


@main_bp.route("/send-contact", methods=["POST"])
def send_contact():
    try:
        name = request.form.get("name")
        phone = request.form.get("phone")
        message_text = request.form.get("message")

        msg = Message(
            subject="Новая заявка с сайта",
            recipients=["info@krepfund.ru"],
            body=f"""
            Новая заявка с сайта:

            Имя: {name}
            Телефон: {phone}

            Сообщение:
            {message_text}
                    """
        )

        mail.send(msg)

        return jsonify({
            "status": "ok",
            "message": "Заявка успешно отправлена!"
        })

    except Exception as e:
        return jsonify(status="error", error=str(e))


@main_bp.route('/check_title')
def check_title():
    title = request.args.get('title', '').strip()
    exists = Project.query.filter_by(title=title).first() is not None
    return jsonify({'exists': exists})


# IMAGE COMPRESSORS
def ensure_hero_webp(input_path, overwrite=True):
    original_file_path = os.path.join(current_app.static_folder, input_path)
    bg_dir = os.path.join(current_app.static_folder, 'images', 'hero_bg')

    bg_hd_path = os.path.join(bg_dir, 'bg_hd.webp')
    bg_lq_path = os.path.join(bg_dir, 'bg_lq.webp')

    # Создаём директорию, если её нет
    os.makedirs(bg_dir, exist_ok=True)

    # ---- УСЛОВИЕ СОЗДАНИЯ ----
    need_regenerate = (
        overwrite or
        not os.path.exists(bg_hd_path) or
        not os.path.exists(bg_lq_path)
    )

    if need_regenerate:
        # HD ---
        hd_img = Image.open(original_file_path)
        hd_img.save(
            bg_hd_path,
            "WEBP",
            quality=50,
            method=6,
            lossless=False
        )

        # LQ / BLUR ---
        lq_img = hd_img.resize((100, 100), Image.LANCZOS)
        lq_img = lq_img.filter(ImageFilter.GaussianBlur(1))
        lq_img.save(
            bg_lq_path,
            "WEBP",
            quality=15,
            method=6,
            lossless=False
        )

    # Возвращаем пути для HTML
    return [
        os.path.join('static', 'images', 'hero_bg', 'bg_lq.webp'),
        os.path.join('static', 'images', 'hero_bg', 'bg_hd.webp'),
    ]



@main_bp.route('/img_blur/<path:filename>')
def img_blur(filename):
    full_path = os.path.join(current_app.static_folder, filename)

    if not os.path.exists(full_path):
        abort(404)

    img = Image.open(full_path)

    # 1. Уменьшаем картинку (это критично для blur)
    img.thumbnail((100, 100))  # ширина максимум 50px

    # 2. Сохраняем в памяти
    buffer = io.BytesIO()
    img.save(
        buffer,
        format="WEBP",
        quality=20,  # качество 10–20 идеально
        method=6
    )
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/webp",
        download_name="blur.webp"
    )


@main_bp.route('/img_lq/<path:filename>')
def img_card_lq(filename):
    full_path = os.path.join(current_app.static_folder, filename)
    if not os.path.exists(full_path):
        abort(404)

    img = Image.open(full_path)

    # Уменьшаем до очень маленькой высоты (для blur)
    target_height = 500
    w, h = img.size
    ratio = target_height / h
    new_w = int(w * ratio)
    img = img.resize((new_w, target_height), Image.LANCZOS)

    # Добавляем размытие для плавного вида при растягивании
    img = img.filter(ImageFilter.GaussianBlur(radius=2))

    buffer = io.BytesIO()
    # Минимальное качество — чтобы вес был максимально маленький
    img.save(buffer, format="WEBP", quality=15, method=6)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/webp",
        as_attachment=False,
        download_name="blur.webp"
    )


@main_bp.route('/img_resize/<path:filename>')
def img_card_hd(filename):
    full_path = os.path.join(current_app.static_folder, filename)
    if not os.path.exists(full_path):
        abort(404)

    img = Image.open(full_path)

    # Задаём целевую высоту (например, для карточек)
    target_height = 600
    w, h = img.size
    ratio = target_height / h
    new_w = int(w * ratio)

    # Уменьшаем разрешение, сохраняя пропорции

    img = img.resize((new_w, target_height), Image.LANCZOS)

    buffer = io.BytesIO()
    # Сохраняем качество максимально
    img.save(buffer, "WEBP", quality=20, method=6, lossless=False)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/webp",
        as_attachment=False,
        download_name="resized.webp"
    )


# TEST
@main_bp.route('/test')
def test():
    project = Project.query.first()
    projects = Project.query.all()
    return render_template('____test.html', project=project, projects=projects)
