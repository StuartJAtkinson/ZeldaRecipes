import cv2
import numpy as np
import pytesseract
import re
import os
from typing import List, Dict

def process_image(cells: List[np.ndarray]) -> List[Dict]:
    """Process image cells and extract ingredient information."""
    ingredients = []
    for i, cell in enumerate(cells):
        # Extract quantity using OCR
        gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        quantity_text = pytesseract.image_to_string(thresh, config='--psm 6 -c tessedit_char_whitelist=0123456789x')
        
        # Extract quantity number
        quantity_match = re.search(r'x(\d+)', quantity_text)
        quantity = int(quantity_match.group(1)) if quantity_match else 0

        # Save the cell image
        image_path = f'ingredient_images/ingredient_{i+1}.png'
        cv2.imwrite(image_path, cell)

        ingredient = {
            'name': f'Ingredient_{i+1}',
            'quantity': quantity,
            'image': image_path
        }
        
        ingredients.append(ingredient)

    return ingredients