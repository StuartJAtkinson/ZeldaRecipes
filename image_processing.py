import cv2
import numpy as np
import pytesseract
import re
from typing import List, Dict

def process_image(image: np.ndarray) -> List[Dict]:
    """Process a 4x5 grid image and extract ingredient information."""
    height, width = image.shape[:2]
    cell_height, cell_width = height // 4, width // 5
    ingredients = []

    for row in range(4):
        for col in range(5):
            # Extract each cell
            cell = image[row*cell_height:(row+1)*cell_height, 
                         col*cell_width:(col+1)*cell_width]
            
            # Focus on the bottom left corner for text
            text_region = cell[int(cell_height*0.75):, :int(cell_width*0.25)]
            
            # Convert to grayscale
            gray = cv2.cvtColor(text_region, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            
            # Define pytesseract configuration
            config = '--psm 7 --oem 3 -c tessedit_char_whitelist=x0123456789'
            
            # Extract quantity using OCR
            quantity_text = pytesseract.image_to_string(thresh, config=config)
            
            # Extract quantity number
            quantity_match = re.search(r'x(\d+)', quantity_text)
            quantity = int(quantity_match.group(1)) if quantity_match else 0

            # Save the cell image
            image_path = f'ingredient_images/ingredient_{row*5+col+1}.png'
            cv2.imwrite(image_path, cell)

            ingredient = {
                'name': f'Ingredient_{row*5+col+1}',
                'quantity': quantity,
                'image': image_path
            }
            
            ingredients.append(ingredient)

    cv2.destroyAllWindows()  # Close all OpenCV windows
    return ingredients