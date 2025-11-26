from flask import blueprints, jsonify, abort, Blueprint
from flask_login import login_required, current_user
from .models import User, Project
from . import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/admin/')
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)
    return "Admin dashboard"

@admin_bp.route('/admin/add_project')
@login_required
def add_project(id):
    if not current_user.is_admin:
        abort(403)

    return "OK", 201

# API route
@admin_bp.route('/api/project/<int:project_id>', methods=['DELETE'])
@login_required
def api_delete_project(project_id):
    if not current_user.is_admin:
        abort(403)

    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify(status='ok')

