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

    def upload_image(self):
        """Handle image upload and display."""
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
        if hasattr(self, 'image_path'):
            grid_selector = GridSelector(self.master, self.image_path)
            cells = grid_selector.get_cells()
            ingredients = process_image(cells)
            ingredient_display = IngredientDisplay(self.master, ingredients)
            confirmed_ingredients = ingredient_display.get_confirmed_ingredients()
            categorized_ingredients = categorize_ingredients(confirmed_ingredients)
            recipes = generate_recipes(categorized_ingredients)
            recipe_attributes = calculate_attributes(recipes)
            self.display_results(recipe_attributes)

    def display_results(self, recipe_attributes):
        """Display the recipe attributes in the result text area."""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, json.dumps(recipe_attributes, indent=2))