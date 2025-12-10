import os.path
import io, os

from flask import Blueprint, render_template, redirect, current_app, request, jsonify, flash, send_file, abort, url_for
from flask import jsonify
from flask_mail import Message

from PIL import Image, ImageFilter

from app.models import Project, ProjectImages
from app import mail

main_bp = Blueprint('main', __name__)

def ensure_hero_webp(input_path):
    original_file_path = os.path.join(current_app.static_folder, input_path)
    bg_hd_path = os.path.join(current_app.static_folder, 'images', 'hero_bg', 'bg_hd.webp')
    bg_lq_path = os.path.join(current_app.static_folder, 'images', 'hero_bg', 'bg_lq.webp')

    if not (os.path.exists(bg_hd_path) and os.path.exists(bg_lq_path)):
        hero_bg_dir_path = os.path.join(current_app.static_folder, 'images', 'hero_bg')
        os.makedirs(hero_bg_dir_path, exist_ok=True)

        # HD
        hd_img = Image.open(original_file_path)
        hd_img.save(bg_hd_path, "WEBP", quality=20, method=6, lossless=False)

        # BLUR
        lq_img = Image.open(bg_hd_path)
        lq_img = lq_img.resize((100, 100), Image.LANCZOS)
        lq_img = lq_img.filter(ImageFilter.GaussianBlur(1))  # размытие
        lq_img.save(bg_lq_path, "WEBP", quality=15, method=6, lossless=False)



        # lq_img = Image.open(original_file_path)
        # lq_img = lq_img.resize((20,20), Image.LANCZOS)  # уменьшаем до миниатюры
        # # img = img.filter(ImageFilter.GaussianBlur(1))
        # lq_img.save(bg_lq_path, "WEBP", quality=20)

    hd_img_relative_path = os.path.join('static', 'images', 'hero_bg', 'bg_hd.webp')
    lq_img_relative_path = os.path.join('static', 'images', 'hero_bg', 'bg_lq.webp')

    images_path = [lq_img_relative_path, hd_img_relative_path]
    print(images_path)
    return images_path


@main_bp.route('/')
def index():
    projects = Project.query.all()
    img_url = ensure_hero_webp(projects[0].images.first().url)
    return render_template('index.html', projects=projects, hero_bg=img_url)


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


# IMAGE COMPRESSORS
@main_bp.route('/img_comp/<path:filename>')
def img_comp(filename):
    full_path = os.path.join(current_app.static_folder, filename)
    if not os.path.exists(full_path):
        abort(404)

    img = Image.open(full_path)

    target_height = 500
    w, h = img.size
    ratio = target_height / h
    new_w = int(w * ratio)
    img = img.resize((new_w, target_height), Image.LANCZOS)

    # Добавляем размытие для плавного вида при растягивании
    img = img.filter(ImageFilter.GaussianBlur(radius=2))

    buffer = io.BytesIO()

    img.save(buffer, format="WEBP", quality=30, method=6, lossless=False)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/webp",
        as_attachment=False,
        download_name="comp.webp"
    )

@main_bp.route('/img_lq/<path:filename>')
def img_lq(filename):
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
        quality=20,    # качество 10–20 идеально
        method=6
    )
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/webp",
        download_name="blur.webp"
    )




@main_bp.route('/img_resize/<path:filename>')
def img_resize(filename):
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
