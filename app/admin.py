import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import House, HouseImage
from .admin_views import HouseImageAdmin


def init_admin(app, db):
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')

    admin.add_view(ModelView(House, db.session))

    upload_dir = os.path.join(app.root_path, 'static/uploads/houses')
    admin.add_view(HouseImageAdmin(HouseImage, db.session, upload_path=upload_dir))

    return admin
