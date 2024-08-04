# ZeldaRecipes

ZeldaRecipes is an application that allows users to upload an image of the Zelda ingredients tab, processes the image to extract ingredient information, and generates recipes based on the extracted data.

## Features

1. **Image Upload**: Users can upload an image of the Zelda ingredients tab.
2. **OCR Processing**: The application uses Optical Character Recognition (OCR) to extract ingredient names and quantities from the uploaded image.
3. **Ingredient Categorization**: Extracted ingredients are categorized based on predefined categories.
4. **Recipe Generation**: The application generates unique permutations of recipes based on the categorized ingredients.
5. **Attribute Calculation**: It calculates relevant attributes for the generated recipes, such as health, stamina, and status effects.

## Requirements

- Python 3.x
- Required libraries:
  - OpenCV
  - Pillow
  - Pytesseract
  - Tkinter (comes with Python)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd ZeldaRecipes
   ```

2. **Install Dependencies**:
   Make sure you have the required libraries installed. You can use pip to install them:
   ```bash
   pip install opencv-python pytesseract pillow
   ```

   Ensure you have Tesseract OCR installed on your system. You can download it from [here](https://github.com/tesseract-ocr/tesseract) and set the path in the `ui.py` file.

## Running the Application

To run the application, execute the following command:


bash
python ui.py

### Step-by-Step Usage

1. **Upload Image**:
   - Click the "Upload Image" button to select an image file of the Zelda ingredients tab from your computer.

2. **Process Image**:
   - After uploading, click the "Process Image" button. The application will process the image to extract ingredient information using OCR.

3. **Define Grid**:
   - A new window will open where you can define the grid for the ingredients. Click and drag to select the area containing the ingredients.

4. **Confirm Grid**:
   - After defining the grid, click the "Confirm Grid" button. The application will extract the ingredients from the selected area.

5. **Verify Ingredients**:
   - A new window will display the extracted ingredients. You can verify and edit the ingredient names and quantities if needed.

6. **Generate Recipes**:
   - Once you confirm the ingredients, the application will generate recipes based on the extracted data and display the relevant attributes.

7. **Close Application**:
   - You can close the application by clicking the close button on the window. The application will clean up any temporary files created during the process.

## Contributing

Feel free to contribute to the project by submitting issues or pull requests.

## License

This project is licensed under the MIT License.