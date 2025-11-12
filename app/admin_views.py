import os
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField


class HouseImageAdmin(ModelView):
    def __init__(self, model, session, upload_path, **kwargs):
        self.upload_path = upload_path
        super().__init__(model, session, **kwargs)

    form_columns = ['house', 'image_path']

    def _form_extra_fields(self):
        return {
            'image_path': ImageUploadField(
                'Изображение',
                base_path=self.upload_path,
                relative_path='uploads/houses/',
                thumbnail_size=(200, 200, True)
            )
        }

    form_extra_fields = property(_form_extra_fields)
