import os

from flask import jsonify, abort, Blueprint, render_template, redirect
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from .models import Project, ProjectImages
from .forms import ProjectForm
from . import db

admin_bp = Blueprint('admin', __name__)

# === ADMIN ===
@admin_bp.route('/admin/')
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)

    projects = Project.query.all()
    form = ProjectForm()
    return render_template('admin.html', projects=projects, form=form)

    return "Admin dashboard"

# === ADD PROJECT ===
@admin_bp.route('/admin/add_project')
@login_required
def add_project(id):
    if not current_user.is_admin:
        abort(403)
    return "OK", 201

# === EDIT PROJECT ===
@admin_bp.route('/admin/edit_project/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    if not current_user.is_admin:
        abort(403)

    project = Project.query.get_or_404(id)
    projects = Project.query.all()
    images = project.images.all()
    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        form.populate_obj(project)


        files = form.img_files.data

        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(project.images_directory_path, filename)
                file.save(filepath)
                image = ProjectImages(project_id=project.id, filename=filename)

                db.session.add(image)
                # db.session.commit()

        db.session.commit()
        # form = ProjectForm()
        return redirect('/admin/')
    existing_files = [img.filename for img in images]
    return render_template('edit_project.html', projects=projects, project=project, form=form, images=images, existing_files=existing_files)

# === API == DELETE PROJECT ===
@admin_bp.route('/api/project/<int:project_id>', methods=['DELETE'])
@login_required
def api_delete_project(project_id):
    if not getattr(current_user, "is_admin", False):
        return jsonify({"error": "access_denied"}), 403

    project = Project.query.get_or_404(project_id)

    db.session.delete(project)
    db.session.commit()

    return jsonify({"status": "ok"}, 200)

# === API === DELETE IMAGES
@admin_bp.route("/delete_image/<int:image_id>", methods=["DELETE"])
@login_required
def delete_image(image_id):
    if not getattr(current_user, "is_admin", False):
        return jsonify({"error": "access_denied"}), 403

    image = ProjectImages.query.get(image_id)

    if not image:
        return "Not found", 404
    try:
        os.remove(os.path.join(image.full_path))
    except FileNotFoundError as e:
        print(e)
        return f"{e}"

    db.session.delete(image)
    db.session.commit()

    return "OK", 200
