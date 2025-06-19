# Screenshot Comment Generator

A Chrome extension that allows users to capture portions of their screen and generate AI-powered comments about the captured content.

## Features

- **Region Selection**: Draw, resize, and drag a selection rectangle to capture specific areas of the screen.
- **Screenshot Capture**: Capture the selected region using Chrome's API.
- **Comment Generation**: Generate AI-powered comments about the captured screenshot.
- **Caption Support**: Add optional captions to provide context for the AI.
- **Edit & Copy**: Edit generated comments or copy them to the clipboard.

## Installation

### Chrome Extension

1. Download or clone this repository
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable "Developer mode" by clicking the toggle in the top-right corner
4. Click "Load unpacked" and select the `chrome-extension` folder from this repository
5. The extension should now be installed and visible in your Chrome toolbar

### Python Backend

The extension relies on a Python server for comment generation. To set up the server:

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```
   pip install flask flask-cors pillow
   ```
3. Update the `apiEndpoint` in `background.js` to point to your server
4. Run the server:
   ```
   python comment_generator.py
   ```
   
The server will start on `http://localhost:8000` by default.

## Usage

1. Click the extension icon in your Chrome toolbar
2. Click the "Select Region" button in the popup
3. Draw a rectangle around the area you want to capture
   - You can adjust the selection by dragging its borders or corners
   - Click "Capture" when you're ready
4. Add an optional caption to provide context
5. Click "Generate Comment" to send the screenshot to the AI
6. View, copy, or edit the generated comment

## Configuration

### Extension Settings

You can modify the following settings:

- API endpoint: Update `apiEndpoint` in `background.js` to point to your server
- Selection appearance: Customize the selection rectangle by modifying `content.css`

### Server Settings

The Python server has the following configuration options in `comment_generator.py`:

- `DEBUG`: Set to `False` in production
- `HOST`: Server host address (default: `0.0.0.0`)
- `PORT`: Server port (default: `8000`)

## Development

### Project Structure

```
chrome-extension/
├── manifest.json       # Extension manifest
├── popup.html          # Popup UI
├── js/
│   ├── background.js   # Background service worker
│   ├── content.js      # Content script for selection
│   ├── popup.js        # Popup UI logic
│   └── utils.js        # Utility functions
├── styles/
│   ├── content.css     # Content script styles
│   └── popup.css       # Popup UI styles
├── images/             # Icons and images
├── tests/              # Test files
└── comment_generator.py # Python API for comment generation
```

### Building for Production

1. Update the version in `manifest.json`
2. Remove any console.log statements
3. Ensure the API endpoint is set correctly
4. Create a ZIP file of the extension directory
5. Upload to the Chrome Web Store

## Testing

### Manual Testing

Test the extension on different websites, with different screen sizes, and with various selection regions.

### Automated Testing

Run the unit tests:

```
# Test instructions will go here
```

## Security Considerations

- All communication with the backend is done using HTTPS
- User data is not stored permanently
- The extension requests only the necessary permissions

## Troubleshooting

- **Extension doesn't load**: Check for errors in the Chrome extension page and console
- **Selection doesn't appear**: Ensure the content script is properly injected
- **API connection fails**: Verify that the Python server is running and accessible

## License

This project is licensed under the MIT License - see the LICENSE file for details.
