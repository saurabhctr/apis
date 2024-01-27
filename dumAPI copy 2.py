from flask import Flask, request, jsonify
from functools import wraps
import base64
import re

app = Flask(__name__)
#test change
# Define your API key here
#ad here
API_KEY = '1234'  # Replace with your actual API key

def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        provided_key = request.headers.get('Authorization')

        if not provided_key or not validate_api_key(provided_key):
            return jsonify({'error': 'Unauthorized access'}), 401

        return view_function(*args, **kwargs)

    return decorated_function

def validate_api_key(provided_key):
    try:
        # Extract the base64 encoded part after 'Basic '
        api_key_encoded = provided_key.split(' ')[1]
        # Decode the base64 string
        api_key_decoded = base64.b64decode(api_key_encoded).decode('utf-8')
        # Check if the decoded key matches the expected API key
        return api_key_decoded == API_KEY
    except Exception as e:
        print(e)
        return False

def remove_special_chars(input_string):
    # Remove special characters using regex
    return re.sub(r'[^a-zA-Z0-9 ]+', '', input_string)

@app.route('/api/square', methods=['GET'])
@require_api_key
def square():
    input_data = request.args.get('input')

    if input_data is None:
        return jsonify({'error': 'Please provide input'}), 400

    cleaned_input = remove_special_chars(input_data)

    if cleaned_input.isdigit():
        result = int(cleaned_input) ** 2
    elif cleaned_input.isalpha():
        result = cleaned_input.upper()
    else:
        result = 'alphanum'

    return jsonify({'result': result})

@app.route('/api/reverse', methods=['POST'])
@require_api_key
def reverse():
    input_data = request.get_json()

    if input_data is None:
        return jsonify({'error': 'Please provide input as JSON'}), 400

    reversed_data = {v: k for k, v in input_data.items()}

    return jsonify({'result': reversed_data})

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
