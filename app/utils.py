import os.path
from flask import current_app


def delete_house_files(house):
    for img in house.images:
        full_path = os.path.join(
            current_app.static_folder, img.url
        )
        if os.path.exists(full_path):
            os.remove(full_path)