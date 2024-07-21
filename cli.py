import cv2
import pytesseract
from PIL import Image
import json
from image_processing import process_image
from ingredient_processor import process_ingredients, categorize_ingredients
from recipe_generator import generate_recipes
from attribute_calculator import calculate_attributes
from image_downloader import download_ingredient_images

def main():
    """Run the command-line interface version of the application."""
    # 1. Image input and OCR
    image = cv2.imread('zelda_ingredients.jpg')
    text = pytesseract.image_to_string(Image.fromarray(image))
    
    # 2. Convert to JSON
    ingredients = process_ingredients(text)
    
    # 3. Download ingredient images
    ingredients_with_images = download_ingredient_images(ingredients)
    
    # 4. Categorize ingredients
    categorized_ingredients = categorize_ingredients(ingredients_with_images)
    
    # 5. Generate unique recipe permutations
    recipes = generate_recipes(categorized_ingredients)
    
    # 6. Calculate attributes for recipes
    recipe_attributes = calculate_attributes(recipes)
    
    # Output results
    print(json.dumps(recipe_attributes, indent=2))

    # TODO: Implement user interface for image upload and JSON display

if __name__ == "__main__":
    main()