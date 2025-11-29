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

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)


@main_bp.route('/details/<int:id>')
def details(id):
    project = Project.query.get(id)
    first_image_url = os.path.join(current_app.static_folder, project.images.first().url)
    print(f"HERE !!! = = {first_image_url}")

    projects = Project.query.all()
    return render_template('project_details.html', project=project, first_image_url=first_image_url, projects=projects)

#TEST
@main_bp.route('/details/test')
def details_test():
    project = Project.query.get(1)
    return render_template('test/prises-test.html', project=project)

# ==== ADMIN =========
# @main_bp.route('/admin/')
# def admin():
#     projects = Project.query.all()
#     form = ProjectForm()
#     return render_template('admin.html', projects=projects, form=form)
#
#
# @main_bp.route('/admin/add_project', methods=['POST'])
# def add_project():
#     form = ProjectForm()
#
#     if not form.validate_on_submit():
#         flash("Ошибка формы", "danger")
#         return redirect('/admin/')
#
#     new_project = Project(
#         title=form.title.data,
#         description=form.description.data,
#         square=form.square.data,
#         size=form.size.data,
#         price_base=form.price_base.data,
#         price_with_communications=form.price_with_communications.data,
#         price_ready=form.price_ready.data,
#         mortgage_price_per_month=form.mortgage_price_per_month.data
#     )
#
#     db.session.add(new_project)
#     db.session.commit()
#
#     # 🔥 100% работает со множественными файлами
#     files = request.files.getlist('img_files')
#
#     for file in files:
#         if file and file.filename:
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(new_project.images_directory_path, filename)
#             file.save(filepath)
#
#             image = ProjectImages(project_id=new_project.id, filename=filename)
#             db.session.add(image)
#
#     db.session.commit()
#
#     flash("Проект успешно добавлен!", "success")
#     return redirect('/admin/')



# EDIT PROJECT
# @main_bp.route('/admin/edit_project/<int:id>', methods=['GET', 'POST'])
# def edit_project(id):
#     project = Project.query.get_or_404(id)
#     projects = Project.query.all()
#     images = project.images.all()
#     form = ProjectForm(obj=project)
#
#     if form.validate_on_submit():
#         form.populate_obj(project)
#
#
#         files = form.img_files.data
#
#         for file in files:
#             if file and file.filename:
#                 filename = secure_filename(file.filename)
#                 filepath = os.path.join(project.images_directory_path, filename)
#                 file.save(filepath)
#                 image = ProjectImages(project_id=project.id, filename=filename)
#
#                 db.session.add(image)
#
#                 db.session.commit()
#
#         db.session.commit()
#         form = ProjectForm()
#         return redirect('/admin/')
#     existing_files = [img.filename for img in images]
#     return render_template('edit_project.html', projects=projects, project=project, form=form, images=images, existing_files=existing_files)


# === JS API ================================
# @main_bp.route('/api/project/<int:project_id>', methods=['DELETE'])
# @login_required
# def api_delete_project(project_id):
#     if not getattr(current_user, "is_admin", False):
#         return jsonify({"error": "access_denied"}), 403
#
#     project = Project.query.get_or_404(project_id)
#
#     db.session.delete(project)
#     db.session.commit()
#
#     return jsonify({"status": "ok"}, 200)

# @main_bp.route("/delete_image/<int:image_id>", methods=["DELETE"])
# def delete_image(image_id):
#     image = ProjectImages.query.get(image_id)
#
#     if not image:
#         return "Not found", 404
#     try:
#         os.remove(os.path.join(image.full_path))
#     except FileNotFoundError as e:
#         print(e)
#         return f"{e}"
#
#     # Удаляем запись из БД
#     db.session.delete(image)
#     db.session.commit()
#
#     return "OK", 200





@main_bp.route('/check_title')
def check_title():
    title = request.args.get('title', '').strip()
    exists = Project.query.filter_by(title=title).first() is not None
    return jsonify({'exists': exists})
