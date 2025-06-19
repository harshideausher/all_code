# Screenshot Comment Generator - Firefox Version

This is the Firefox version of the Screenshot Comment Generator browser extension. It allows you to select a region of the screen, capture it, and generate AI comments for code screenshots.

## Conversion from Chrome to Firefox

This extension has been converted from a Chrome extension to a Firefox extension. The main changes include:

1. Updated the `manifest.json` file to use Manifest V2 instead of V3
2. Changed browser API calls from `chrome.*` to `browser.*`
3. Updated background scripts to use Firefox-compatible APIs
4. Modified promise handling in API calls to use `.then()/.catch()` instead of callback functions

## Installation

### Temporary Installation (for Development)

1. Open Firefox and navigate to `about:debugging`
2. Click "This Firefox" in the left sidebar
3. Click "Load Temporary Add-on..."
4. Navigate to the extension directory and select the `manifest.json` file

### Packaging for Distribution

To create a distributable package:

1. Zip all the extension files (make sure manifest.json is at the root of the zip file)
2. Rename the zip file to have a `.xpi` extension
3. You can then submit the `.xpi` file to the [Firefox Add-ons site](https://addons.mozilla.org/)

## Usage

1. Click the extension icon in the toolbar
2. Click "Select Region" to select an area of the screen
3. Use the selection tool to select the area you want to capture
4. Click "Capture" to capture the selected area
5. Optionally add a caption
6. Click "Generate Comment" to generate an AI comment for the screenshot
7. Edit, copy, or regenerate the comment as needed

## Server Connection

This extension requires a local Python server to process the screenshots and generate comments. Make sure the server is running on `http://localhost:8000` before using the extension.

To start the server:
```
python comment_generator.py
```

## Differences from Chrome Version

The Firefox version works similarly to the Chrome version, but with a few differences:

1. Firefox uses a different storage mechanism, but the API is compatible
2. The popup handling is slightly different
3. Content script injection uses a different approach in Firefox

## Troubleshooting

- If you encounter issues with capturing screenshots, make sure you have granted the necessary permissions to the extension
- If the comment generation fails, check that the Python server is running correctly
- For other issues, check the Firefox browser console (Ctrl+Shift+J or Cmd+Shift+J) for error messages 