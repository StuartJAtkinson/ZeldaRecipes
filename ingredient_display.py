import tkinter as tk
from PIL import Image, ImageTk
from typing import List, Dict
from tkinter import scrolledtext
import cv2
import pytesseract
import re

class IngredientDisplay:
    def __init__(self, master: tk.Tk, ingredients: List[Dict]):
        """Initialize the ingredient display and verification window."""
        self.master = master
        self.ingredients = ingredients
        self.ingredient_window = tk.Toplevel(master)
        self.ingredient_window.title("Verify Ingredients")
        self.ingredient_window.geometry("800x600")

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface for ingredient display and verification."""
        canvas = tk.Canvas(self.ingredient_window)
        scrollbar = tk.Scrollbar(self.ingredient_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for i, ingredient in enumerate(self.ingredients):
            frame = tk.Frame(scrollable_frame)
            frame.pack(pady=10, padx=10, fill="x", expand=True)

            try:
                img = Image.open(ingredient['image'])
                img = img.resize((50, 50), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(frame, image=photo)
                img_label.image = photo
            except FileNotFoundError:
                img_label = tk.Label(frame, text="Image not found")
            img_label.pack(side=tk.LEFT)

            name_var = tk.StringVar(value=ingredient['name'])
            name_entry = tk.Entry(frame, textvariable=name_var, width=20)
            name_entry.pack(side=tk.LEFT, padx=10)

            quantity_var = tk.IntVar(value=ingredient['quantity'])
            quantity_entry = tk.Entry(frame, textvariable=quantity_var, width=5)
            quantity_entry.pack(side=tk.LEFT, padx=10)

            ocr_button = tk.Button(frame, text="Run OCR", command=lambda idx=i: self.run_ocr(idx))
            ocr_button.pack(side=tk.LEFT, padx=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.log_text = scrolledtext.ScrolledText(self.ingredient_window, height=10)
        self.log_text.pack(fill="x", padx=10, pady=10)

        confirm_button = tk.Button(self.ingredient_window, text="Confirm Ingredients", command=self.confirm_ingredients)
        confirm_button.pack(pady=10)

    def run_ocr(self, index):
        cell = self.ingredients[index]['image']
        gray = cv2.cvtColor(cv2.imread(cell), cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        config = '--psm 7 --oem 3 -c tessedit_char_whitelist=x0123456789'
        quantity_text = pytesseract.image_to_string(thresh, config=config)
        self.log_text.insert(tk.END, f"OCR Output for {self.ingredients[index]['name']}: {quantity_text}\n")
        quantity_match = re.search(r'x(\d+)', quantity_text)
        quantity = int(quantity_match.group(1)) if quantity_match else 0
        self.ingredients[index]['quantity'] = quantity

    def get_confirmed_ingredients(self):
        """Get the confirmed ingredients."""
        return self.ingredients

    def confirm_ingredients(self):
        """Confirm the ingredients and close the window."""
        self.ingredient_window.destroy()
        self.master.quit()

    def get_recipe_attributes(self):
        """Process confirmed ingredients and return recipe attributes."""
        # Implementation details...