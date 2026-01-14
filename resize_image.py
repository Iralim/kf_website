import os
from PIL import Image

# Целевая высота
TARGET_HEIGHT = 600

# Поддерживаемые форматы
SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

def resize_image(filepath):
    img = Image.open(filepath)

    w, h = img.size
    ratio = TARGET_HEIGHT / h
    new_w = int(w * ratio)

    img = img.resize((new_w, TARGET_HEIGHT), Image.LANCZOS)

    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_name = f"{base_name}_resized.webp"

    img.save(
        output_name,
        "WEBP",
        quality=20,
        method=6,
        lossless=False
    )

    print(f"✔ {output_name} создан")

def main():
    current_dir = os.getcwd()

    for filename in os.listdir(current_dir):
        if filename.lower().endswith(SUPPORTED_EXTENSIONS):
            try:
                resize_image(os.path.join(current_dir, filename))
            except Exception as e:
                print(f"✖ Ошибка с {filename}: {e}")

if __name__ == "__main__":
    main()
