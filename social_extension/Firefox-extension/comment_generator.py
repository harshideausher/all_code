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
import tempfile
import uuid


from smol_5 import commnet_genrater

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
        
        print(f"Received image data (length: {len(image_data)}), caption: '{caption}'")
        
        # Process with the AI model in smol_5.py
        temp_file_path = None
        try:
            # First, we need to save the base64 image to a temporary file
            temp_file_path = save_base64_to_temp_file(image_data)
            
            # Call the commnet_genrater function with the file path and caption
            print(f"Processing image with AI model: {temp_file_path}")
            comment = commnet_genrater(temp_file_path, caption)
            print(f"Generated comment: {comment}")
            
            # In case the comment is None or empty, provide a fallback
            if not comment:
                comment = "Could not generate a comment for this image. Please try with a different screenshot."
                
        except Exception as e:
            print(f"Error in AI processing: {e}")
            # Return a user-friendly error
            return jsonify({'error': f'Error analyzing image: {str(e)}. Please try with a different screenshot.'}), 500
        finally:
            # Clean up the temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                    print(f"Removed temporary file: {temp_file_path}")
                except Exception as e:
                    print(f"Error removing temp file: {e}")
        
        # Return the generated comment
        response = jsonify({'comment': comment})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 200
    
    except Exception as e:
        print(f"Unhandled error in generate_comment: {str(e)}")
        error_response = jsonify({'error': f'Server error: {str(e)}'})
        error_response.headers['Access-Control-Allow-Origin'] = '*'
        return error_response, 500

def save_base64_to_temp_file(base64_image):
    """
    Save a base64 encoded image to a temporary file and return the file path.
    """
    try:
        # Extract the base64 data from the data URL
        if ',' in base64_image:
            base64_data = base64_image.split(',', 1)[1]
        else:
            base64_data = base64_image
        
        # Clean the base64 string
        base64_data = base64_data.strip()
        # Add padding if needed
        padding = 4 - (len(base64_data) % 4) if len(base64_data) % 4 != 0 else 0
        base64_data += '=' * padding
        
        # Decode the base64 data
        try:
            image_bytes = base64.b64decode(base64_data)
        except Exception as e:
            print(f"Base64 decoding error: {e}")
            # Try using PIL to open the image directly from base64 data
            img = Image.open(io.BytesIO(base64.b64decode(base64_data + '===='[:padding])))
            
            # Create a temporary file
            temp_dir = tempfile.gettempdir()
            file_name = f"temp_image_{uuid.uuid4().hex}.png"
            file_path = os.path.join(temp_dir, file_name)
            
            # Save using PIL
            img.save(file_path, format='PNG')
            print(f"Saved image using PIL to: {file_path}")
            return file_path
        
        # Verify the image data
        try:
            Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            print(f"Invalid image data: {e}")
            raise ValueError("The base64 data could not be decoded as a valid image")
        
        # Create a temporary file
        temp_dir = tempfile.gettempdir()
        file_name = f"temp_image_{uuid.uuid4().hex}.png"
        file_path = os.path.join(temp_dir, file_name)
        
        # Save the image to the temporary file
        with open(file_path, 'wb') as f:
            f.write(image_bytes)
        
        print(f"Saved base64 image to: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error in save_base64_to_temp_file: {str(e)}")
        raise

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

if __name__ == '__main__':
    print("Starting comment generator server on http://localhost:8000")
    print("Using AI vision model from smol_5.py")
    app.run(host=HOST, port=PORT, debug=DEBUG) 