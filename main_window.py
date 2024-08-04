import sys
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from grid_selection import GridSelector
from ingredient_display import IngredientDisplay
from image_processing import process_image
import json
from ingredient_processor import categorize_ingredients
from recipe_generator import generate_recipes
from attribute_calculator import calculate_attributes
import cv2
import os
import shutil

class ZeldaRecipesUI:
    def __init__(self, master: tk.Tk):
        """Initialize the main application window."""
        self.master = master
        master.title("Zelda Recipes")
        master.state('zoomed')

        self.upload_button = tk.Button(master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.image_label = tk.Label(master)
        self.image_label.pack()

        self.process_button = tk.Button(master, text="Process Image", command=self.process_image)
        self.process_button.pack()

        self.result_text = tk.Text(master, height=20, width=50)
        self.result_text.pack()

        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def upload_image(self):
        """Handle image upload and display."""
        self.delete_ingredient_images()  # Delete directory at the start
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.image_path = file_path

    def process_image(self):
        """Process the uploaded image and display results."""
        self.delete_ingredient_images()  # Delete directory at the start
        if hasattr(self, 'image_path'):
            # Preprocess the image
            self.original_image = cv2.imread(self.image_path)
            self.original_image = self.preprocess_image(self.original_image)
            
            grid_selector = GridSelector(self.master, self.image_path)
            cells = grid_selector.get_cells()
            ingredients = process_image(cells)
            ingredient_display = IngredientDisplay(self.master, ingredients)
            confirmed_ingredients = ingredient_display.get_confirmed_ingredients()
            categorized_ingredients = categorize_ingredients(confirmed_ingredients)
            recipes = generate_recipes(categorized_ingredients)
            recipe_attributes = calculate_attributes(recipes)
            self.display_results(recipe_attributes)
            self.close_resources()

    def preprocess_image(self, image):
        """Preprocess the image to enhance it for OCR."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 11, 2)
        return thresh

    def display_results(self, recipe_attributes):
        """Display the recipe attributes in the result text area."""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, json.dumps(recipe_attributes, indent=2))

    def close_resources(self):
        # Close any open file handles or resources
        cv2.destroyAllWindows()
        # Add any other necessary cleanup operations

    def delete_ingredient_images(self):
        folder_path = 'ingredient_images'
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
            os.rmdir(folder_path)
            print(f"Deleted {folder_path} folder")
        else:
            print(f"{folder_path} folder does not exist")

    def on_closing(self):
        """Handle the window close event."""
        self.delete_ingredient_images()
        self.master.destroy()