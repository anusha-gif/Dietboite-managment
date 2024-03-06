from flask import Flask, request, render_template
import pandas as pd
import re
from io import StringIO
import requests

from flask import jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('full.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    if not file:
        return 'No file uploaded.'

    try:
        content = file.read().decode('utf-8')
        df = pd.read_csv(StringIO(content))

        ingredient_counts = {}
        for index, row in df.iterrows():
            ingredients = row['Ingredients'].split('\n')
            for item in ingredients:
                matches = re.findall(r'([a-zA-Z\s]+)\s*-\s*([\d\.]+)\s*(?:g|gm)?', item)
                for match in matches:
                    item_name, item_quantity = match
                    item_name = item_name.strip()
                    item_quantity = float(item_quantity)

                    if item_name in ingredient_counts:
                        ingredient_counts[item_name] += item_quantity
                    else:
                        ingredient_counts[item_name] = item_quantity

        result = ''
        for ingredient, count in ingredient_counts.items():
            result += f'{ingredient}: {count}\n'

        return result

    except Exception as e:
        return f'Error processing the file: {e}'

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import pandas as pd
import re
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('full.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    if not file:
        return 'No file uploaded.'

    try:
        content = file.read()
        df = pd.read_excel(BytesIO(content))

        # Process data and aggregate item quantities
        result = process_data(df)

        return jsonify(result)

    except Exception as e:
        return f'Error processing the file: {e}'

def process_data(df):
    # Create a dictionary to store ingredient counts
    ingredient_counts = {}

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        ingredients = row['Ingredients'].split('\n')
        for item in ingredients:
            # Extracting ingredient name and quantity
            matches = re.findall(r'([a-zA-Z\s]+)\s*-\s*([\d\.]+)\s*(?:g|gm)?', item)
            for match in matches:
                item_name, item_quantity = match
                item_name = item_name.strip()  # Remove extra spaces
                item_quantity = float(item_quantity)  # Convert quantity to float

                # Update ingredient count in the dictionary
                if item_name in ingredient_counts:
                    ingredient_counts[item_name] += item_quantity
                else:
                    ingredient_counts[item_name] = item_quantity

    # Create a list of dictionaries for each item and quantity
    result = [{'Item': item, 'Quantity': quantity} for item, quantity in ingredient_counts.items()]
    return result
@app.route('/generate_general_report', methods=['GET'])
def generate_general_report():
    try:
        # Get data or process the data as needed
        # In this example, we'll generate a sample CSV data
        data = [
            {'Item': 'Apple', 'Quantity': 5},
            {'Item': 'Banana', 'Quantity': 8},
            {'Item': 'Orange', 'Quantity': 12},
        ]

        return jsonify(data)
        

    except Exception as e:
        return f'Error generating general report: {e}' 

if __name__ == '__main__':
    app.run(debug=True)
