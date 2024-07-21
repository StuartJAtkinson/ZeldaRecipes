import os
from shutil import copyfile

def download_ingredient_images(ingredients):
    image_dir = 'ingredient_images'
    os.makedirs(image_dir, exist_ok=True)
    placeholder_image = 'placeholder.png'  # Ensure this file exists in your project directory
    
    for ingredient in ingredients:
        image_path = os.path.join(image_dir, f"{ingredient['name'].lower().replace(' ', '_')}.png")
        copyfile(placeholder_image, image_path)
        ingredient['image'] = image_path
    
    return ingredients