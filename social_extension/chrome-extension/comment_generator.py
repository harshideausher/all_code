import os
import base64
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from PIL import Image
import io
import re
import sys

# Add parent directory to path to import smol_5.py
sys.path.append('..')

# Import the AI comment generator function
try:
    from smol_5 import commnet_genrater
    print("Successfully imported AI comment generator function")
except ImportError as e:
    print(f"Error importing AI module: {e}")
    print("Falling back to basic comment generator")
    commnet_genrater = None

# Create the Flask application
app = Flask(__name__)
# Enable CORS for all routes with Chrome extension specific settings
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type", "Accept"], "methods": ["POST", "OPTIONS"]}})

# Configuration
DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

@app.route('/generate-comment', methods=['POST', 'OPTIONS'])
def generate_comment():
    """
    Endpoint for generating comments based on images and captions.
    Expects a JSON payload with:
    - image: str (base64 encoded image)
    - caption: str (optional caption provided by the user)
    
    Returns:
    - comment: str (the generated comment)
    """
    # Handle preflight requests
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Accept'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        return response
        
    try:
        # Get the request data
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract the image and caption
        image_data = data.get('image')
        caption = data.get('caption', '')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Validate the image data
        if not is_valid_base64_image(image_data):
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Generate a comment using the AI function if available
        if commnet_genrater:
            print("Using AI comment generator")
            comment = commnet_genrater(image_data, caption)
        else:
            print("Using fallback comment generator")
            comment = generate_comment_for_image(image_data, caption)
        
        # Return the generated comment
        response = jsonify({'comment': comment})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        error_response = jsonify({'error': str(e)})
        error_response.headers['Access-Control-Allow-Origin'] = '*'
        return error_response, 500

def is_valid_base64_image(base64_string):
    """
    Validate if the string is a valid base64 image.
    """
    # Check if it's a data URL
    if not re.match(r'^data:image\/[a-zA-Z]+;base64,', base64_string):
        return False
    
    # Remove the data URL prefix
    base64_data = base64_string.split(',')[1]
    
    # Validate base64
    try:
        # Try to decode the base64 data
        image_data = base64.b64decode(base64_data)
        
        # Try to open as an image
        Image.open(io.BytesIO(image_data))
        
        return True
    except Exception:
        return False

def generate_comment_for_image(image_data, caption):
    """
    Fallback comment generator for when the AI module is not available.
    
    In a real implementation, this would likely use a machine learning model or API
    to analyze the image and generate a relevant comment.
    
    For this example, we'll just create a simple placeholder comment.
    """
    # Remove the data URL prefix to get just the base64 string
    base64_data = image_data.split(',')[1]
    
    # Decode the base64 string to get the image bytes
    image_bytes = base64.b64decode(base64_data)
    
    # Open the image using PIL
    image = Image.open(io.BytesIO(image_bytes))
    
    # Get image dimensions
    width, height = image.size
    
    # In a real application, you might use an AI model to generate a comment.
    # For this example, we'll generate a simple comment based on the image size and caption.
    
    if caption:
        generated_comment = f"This image ({width}x{height}) shows {caption}. "
    else:
        generated_comment = f"This is a {width}x{height} image. "
    
    # Add more details
    if width > height:
        generated_comment += "It's a landscape-oriented image, "
    elif height > width:
        generated_comment += "It's a portrait-oriented image, "
    else:
        generated_comment += "It's a square image, "
    
    generated_comment += "which appears to be a screenshot from a web page or application. "
    generated_comment += "The content shows interface elements that would be relevant for a user's task or information."
    
    # Simulate processing time (remove in production)
    time.sleep(1)
    
    return generated_comment

if __name__ == '__main__':
    print("Starting comment generator server on http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    app.run(host=HOST, port=PORT, debug=DEBUG)
