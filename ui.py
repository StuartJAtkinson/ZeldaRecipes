import tkinter
import json
import tkinter.filedialog
import PIL.Image
import PIL.ImageTk
import cv2
import numpy
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from ingredient_processor import process_ingredients, categorize_ingredients
from image_downloader import download_ingredient_images
from recipe_generator import generate_recipes
from attribute_calculator import calculate_attributes
import re
import tkinter.simpledialog
import os

class ZeldaRecipesUI:
    def __init__(self, master):
        self.master = master
        master.title("Zelda Recipes")
        master.state('zoomed')  # Maximize the main window

        self.upload_button = tkinter.Button(master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.image_label = tkinter.Label(master)
        self.image_label.pack()

        self.process_button = tkinter.Button(master, text="Process Image", command=self.process_image)
        self.process_button.pack()

        self.result_text = tkinter.Text(master, height=20, width=50)
        self.result_text.pack()

    def upload_image(self):
        file_path = tkinter.filedialog.askopenfilename()
        if file_path:
            image = PIL.Image.open(file_path)
            image.thumbnail((300, 300))
            photo = PIL.ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.image_path = file_path

    def process_image(self):
        if hasattr(self, 'image_path'):
            self.original_image = cv2.imread(self.image_path)
            self.original_height, self.original_width = self.original_image.shape[:2]
            self.define_grid()

    def define_grid(self):
        self.grid_window = tkinter.Toplevel(self.master)
        self.grid_window.title("Define Grid")
        self.grid_window.state('zoomed')

        self.canvas = tkinter.Canvas(self.grid_window)
        self.canvas.pack(fill=tkinter.BOTH, expand=True)

        img = PIL.Image.open(self.image_path)
        img_resized, self.scale_factor = self.resize_image(img)
        self.tk_image = PIL.ImageTk.PhotoImage(img_resized)
        self.image_item = self.canvas.create_image(0, 0, anchor=tkinter.NW, image=self.tk_image)

        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.grid_rect = None

        self.canvas.bind("<ButtonPress-1>", self.start_rect)
        self.canvas.bind("<B1-Motion>", self.draw_rect)
        self.canvas.bind("<ButtonRelease-1>", self.end_rect)

        confirm_button = tkinter.Button(self.grid_window, text="Confirm Grid", command=self.process_grid)
        confirm_button.pack()

    def resize_image(self, img):
        window_width = self.grid_window.winfo_screenwidth()
        window_height = self.grid_window.winfo_screenheight()
        img_ratio = img.width / img.height
        window_ratio = window_width / window_height

        if window_ratio > img_ratio:
            new_height = window_height
            new_width = int(new_height * img_ratio)
        else:
            new_width = window_width
            new_height = int(new_width / img_ratio)

        scale_factor = new_width / img.width
        return img.resize((new_width, new_height), PIL.Image.Resampling.LANCZOS), scale_factor

    def start_rect(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

    def draw_rect(self, event):
        if self.grid_rect:
            self.canvas.delete(self.grid_rect)
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        self.grid_rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="red")

    def end_rect(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)

    def process_grid(self):
        if not self.grid_rect:
            return

        x1, y1, x2, y2 = self.start_x, self.start_y, self.end_x, self.end_y
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        # Get the actual image position and size on the canvas
        img_bbox = self.canvas.bbox(self.image_item)
        img_x, img_y = img_bbox[0], img_bbox[1]

        # Adjust coordinates relative to the image
        x1 = max(0, min((x1 - img_x) / self.scale_factor, self.original_width))
        y1 = max(0, min((y1 - img_y) / self.scale_factor, self.original_height))
        x2 = max(0, min((x2 - img_x) / self.scale_factor, self.original_width))
        y2 = max(0, min((y2 - img_y) / self.scale_factor, self.original_height))

        cell_width = (x2 - x1) / 5
        cell_height = (y2 - y1) / 4

        cells = []
        for row in range(4):
            for col in range(5):
                cell_x1 = int(x1 + col * cell_width)
                cell_y1 = int(y1 + row * cell_height)
                cell_x2 = int(cell_x1 + cell_width)
                cell_y2 = int(cell_y1 + cell_height)

                # Extract cell image
                cell = self.original_image[cell_y1:cell_y2, cell_x1:cell_x2]
                cells.append(cell)

        self.grid_window.destroy()
        self.process_cells(cells)

    def process_cells(self, cells):
        ingredients = []
        os.makedirs('ingredient_images', exist_ok=True)
        for i, cell in enumerate(cells):
            # Extract quantity using OCR
            gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            quantity_text = pytesseract.image_to_string(thresh, config='--psm 6 -c tessedit_char_whitelist=0123456789x')
            
            # Extract quantity number
            quantity_match = re.search(r'x(\d+)', quantity_text)
            quantity = int(quantity_match.group(1)) if quantity_match else 0

            # Save the cell image
            image_path = os.path.join('ingredient_images', f'ingredient_{i+1}.png')
            cv2.imwrite(image_path, cell)

            # For now, use a placeholder name
            ingredient = {
                'name': f'Ingredient_{i+1}',
                'quantity': quantity,
                'image': image_path
            }
            
            ingredients.append(ingredient)

        categorized_ingredients = categorize_ingredients(ingredients)
        recipes = generate_recipes(categorized_ingredients)
        recipe_attributes = calculate_attributes(recipes)
        
        self.result_text.delete(1.0, tkinter.END)
        self.result_text.insert(tkinter.END, json.dumps(recipe_attributes, indent=2))

        # Display the processed ingredients
        self.display_ingredients(ingredients)

    def display_ingredients(self, ingredients):
        ingredient_window = tkinter.Toplevel(self.master)
        ingredient_window.title("Verify Ingredients")
        ingredient_window.geometry("800x600")

        canvas = tkinter.Canvas(ingredient_window)
        scrollbar = tkinter.Scrollbar(ingredient_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tkinter.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for i, ingredient in enumerate(ingredients):
            frame = tkinter.Frame(scrollable_frame)
            frame.pack(pady=10, padx=10, fill="x", expand=True)

            try:
                img = PIL.Image.open(ingredient['image'])
                img = img.resize((50, 50), PIL.Image.Resampling.LANCZOS)
                photo = PIL.ImageTk.PhotoImage(img)
                img_label = tkinter.Label(frame, image=photo)
                img_label.image = photo
            except FileNotFoundError:
                img_label = tkinter.Label(frame, text="Image not found")
            img_label.pack(side=tkinter.LEFT)

            name_var = tkinter.StringVar(value=ingredient['name'])
            name_entry = tkinter.Entry(frame, textvariable=name_var, width=20)
            name_entry.pack(side=tkinter.LEFT, padx=10)

            quantity_var = tkinter.IntVar(value=ingredient['quantity'])
            quantity_entry = tkinter.Entry(frame, textvariable=quantity_var, width=5)
            quantity_entry.pack(side=tkinter.LEFT, padx=10)

            def update_ingredient(index, name_var, quantity_var):
                ingredients[index]['name'] = name_var.get()
                ingredients[index]['quantity'] = quantity_var.get()

            save_button = tkinter.Button(frame, text="Save", command=lambda idx=i, nv=name_var, qv=quantity_var: update_ingredient(idx, nv, qv))
            save_button.pack(side=tkinter.LEFT, padx=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def confirm_ingredients():
            ingredient_window.destroy()
            self.process_confirmed_ingredients(ingredients)

        confirm_button = tkinter.Button(ingredient_window, text="Confirm Ingredients", command=confirm_ingredients)
        confirm_button.pack(pady=10)

    def process_confirmed_ingredients(self, ingredients):
        categorized_ingredients = categorize_ingredients(ingredients)
        recipes = generate_recipes(categorized_ingredients)
        recipe_attributes = calculate_attributes(recipes)
        
        self.result_text.delete(1.0, tkinter.END)
        self.result_text.insert(tkinter.END, json.dumps(recipe_attributes, indent=2))

root = tkinter.Tk()
app = ZeldaRecipesUI(root)
root.mainloop()