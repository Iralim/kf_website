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
    """Главная страница"""
    try:
        # Исправляем путь: убираем os.path.join, передаем просто относительный путь
        hero_images = ensure_hero_images('images/bg_HQ.webp', overwrite=False)
    except Exception as e:
        print(f"Ошибка при создании hero-изображений: {e}")
        # Если что-то пошло не так, используем fallback пути только для WebP
        hero_images = {
            'webp_hd': url_for('static', filename='images/hero_bg/hero.webp'),
            'webp_mobile': url_for('static', filename='images/hero_bg/hero-mobile.webp'),
            'blur': url_for('static', filename='images/hero_bg/hero-blur.webp'),
            # JPG больше не нужны, но оставим для обратной совместимости
            'jpg_hd': None,
            'jpg_mobile': None,
        }

    # Данные для микроразметки
    schema_data = {
        'content_url': request.host_url.rstrip('/') + hero_images['webp_hd'],
        'name': 'Современный энергоэффективный дом под ключ',
        'description': 'Фасад современного каменного дома с панорамными окнами, построенного строительной компанией в Стерлитамаке',
        'keywords': 'строительство домов, каменные дома, энергоэффективные дома, Стерлитамак'
    }

    return render_template('index.html',
                           projects=projects,
                           hero_images=hero_images,
                           schema_data=schema_data)


# IMAGE COMPRESSORS
def ensure_hero_images(input_path, overwrite=True):
    """
    Создаёт все необходимые версии hero-изображения (только WebP)

    Args:
        input_path: путь к исходному изображению относительно static_folder
        overwrite: перезаписывать ли существующие файлы

    Returns:
        dict: словарь с путями ко всем созданным изображениям
    """
    original_file_path = os.path.join(current_app.static_folder, input_path)
    bg_dir = os.path.join(current_app.static_folder, 'images', 'hero_bg')

    # Создаём директорию, если её нет
    os.makedirs(bg_dir, exist_ok=True)

    # Пути только для WebP версий (JPG больше не создаем)
    images = {
        # Основные WebP (десктоп и мобильный)
        'webp_hd': os.path.join(bg_dir, 'hero.webp'),  # десктоп (1920px)
        'webp_mobile': os.path.join(bg_dir, 'hero-mobile.webp'),  # мобильный (768px)
        # Размытая версия для прелоадера
        'blur': os.path.join(bg_dir, 'hero-blur.webp'),  # очень легкая, quality 10-20
    }

    # Проверяем, нужно ли что-то создавать
    need_regenerate = overwrite
    if not need_regenerate:
        for img_path in images.values():
            if not os.path.exists(img_path):
                need_regenerate = True
                break

    if need_regenerate and os.path.exists(original_file_path):
        # Открываем оригинальное изображение
        original = Image.open(original_file_path)

        # Конвертируем в RGB если нужно
        if original.mode in ('RGBA', 'P'):
            original = original.convert('RGB')

        # 1. HD WebP (десктоп) - качество 50%
        hd_img = original.copy()
        if hd_img.width > 1920:
            ratio = 1920 / hd_img.width
            new_height = int(hd_img.height * ratio)
            hd_img = hd_img.resize((1920, new_height), Image.Resampling.LANCZOS)

        hd_img.save(
            images['webp_hd'],
            "WEBP",
            quality=50,
            method=6,  # максимальное сжатие
            lossless=False
        )

        # 2. Mobile WebP (768px) - качество 45%
        mobile_img = original.copy()
        if mobile_img.width > 768:
            ratio = 768 / mobile_img.width
            new_height = int(mobile_img.height * ratio)
            mobile_img = mobile_img.resize((768, new_height), Image.Resampling.LANCZOS)

        mobile_img.save(
            images['webp_mobile'],
            "WEBP",
            quality=45,
            method=6,
            lossless=False
        )

        # 3. BLUR версия (очень легкая, для прелоадера)
        blur_img = original.copy()
        blur_img = blur_img.resize((100, 100), Image.Resampling.LANCZOS)
        blur_img = blur_img.filter(ImageFilter.GaussianBlur(3))

        blur_img.save(
            images['blur'],
            "WEBP",
            quality=10,
            method=6,
            lossless=False
        )

        print(f"✅ Созданы все версии hero-изображения:")
        print(f"   - Десктоп WebP: {os.path.basename(images['webp_hd'])}")
        print(f"   - Мобильный WebP: {os.path.basename(images['webp_mobile'])}")
        print(f"   - Blur прелоадер: {os.path.basename(images['blur'])}")

    # Возвращаем пути для HTML, используя url_for
    return {
        'webp_hd': url_for('static', filename='images/hero_bg/hero.webp'),
        'webp_mobile': url_for('static', filename='images/hero_bg/hero-mobile.webp'),
        'blur': url_for('static', filename='images/hero_bg/hero-blur.webp'),
    }


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
