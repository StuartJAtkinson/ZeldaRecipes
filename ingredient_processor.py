import re

def process_ingredients(text):
    ingredients = []
    lines = text.split('\n')
    for line in lines:
        match = re.match(r'(\w+)\s+(\d+)', line)
        if match:
            name, quantity = match.groups()
            ingredients.append({
                'name': name,
                'quantity': int(quantity),
                'image': f'{name.lower()}.png'  # Assuming image files follow this naming convention
            })
    return ingredients

def categorize_ingredients(ingredients):
    categories = {
        'Fruit': ['Apple', 'Palm Fruit', 'Wildberry', 'Hearty Durian', 'Hydromelon', 'Spicy Pepper', 'Voltfruit', 'Fleet-Lotus Seeds', 'Mighty Bananas'],
        'Mushroom': ['Hylian Shroom', 'Endura Shroom', 'Stamella Shroom', 'Hearty Truffle', 'Big Hearty Truffle', 'Chillshroom', 'Sunshroom', 'Zapshroom', 'Rushroom', 'Razorshroom', 'Ironshroom', 'Silent Shroom'],
        # Add other categories here
    }
    
    for ingredient in ingredients:
        for category, items in categories.items():
            if ingredient['name'] in items:
                ingredient['category'] = category
                break
        else:
            ingredient['category'] = 'Unknown'
    
    return ingredients