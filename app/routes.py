import os.path
from pathlib import Path
import shutil

from flask import Blueprint, render_template, redirect, current_app, request, jsonify, flash
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
    return render_template('details.html', project=project)


# ADMIN
@main_bp.route('/admin/')
def admin():
    projects = Project.query.all()
    form = ProjectForm()
    return render_template('admin.html', projects=projects, form=form)


# ADD PROJECT
@main_bp.route('/admin/add_project', methods=['POST'])
def add_project():
    form = ProjectForm()

    new_project = Project(
        title=form.title.data,
        description=form.description.data,
        square=form.square.data,
        size=form.size.data,
        price_base=form.price_base.data,
        price_with_communications=form.price_with_communications.data,
        price_ready=form.price_ready.data,
        mortgage_price_per_month=form.mortgage_price_per_month.data
    )
    db.session.add(new_project)

    try:
        db.session.commit()

        files = form.img_files.data

        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(new_project.images_directory_path, filename)
                file.save(filepath)
                image = ProjectImages(project_id=new_project.id, filename=filename)

                db.session.add(image)

                db.session.commit()
        flash("Проект успешно добавлен!", "success")
        return redirect('/admin/')
    except IntegrityError:
        db.session.rollback()
        flash("Проект с таким названием уже существует!", "danger")
        return render_template('admin.html', form=form)


# EDIT PROJECT
@main_bp.route('/admin/edit_project/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    project = Project.query.get_or_404(id)
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

                db.session.commit()

        db.session.commit()
        form = ProjectForm()
        return redirect('/admin/')
    return render_template('edit_project.html', project=project, form=form, images=images)


# === JS API ================================
@main_bp.route('/api/project/<int:project_id>', methods=['DELETE'])
def api_delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    db.session.delete(project)
    db.session.commit()

    return {"status": "ok"}


@main_bp.route('/check_title')
def check_title():
    title = request.args.get('title', '').strip()
    exists = Project.query.filter_by(title=title).first() is not None
    return jsonify({'exists': exists})
