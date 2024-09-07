from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Function to clean the text
def clean_text(text):
    pattern = r'[^a-zA-Z0-9\s!@#\$%\^&\*\(\)_\+\-=\[\]\{\}\\|;:\'",<\.>\/\?~]'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

# Define a route to accept POST requests
@app.route('/clean', methods=['POST'])
def clean_text_route():
    # Get the JSON data from the request
    data = request.json
    print(data)
    # Ensure the 'text' key is in the JSON
    if 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    # Clean the text using the defined function
    cleaned = clean_text(data['text'])
    
    # Return the cleaned text as a JSON response
    return jsonify({"cleaned_text": cleaned})

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)
