# Changelog

All notable changes to the Screenshot Comment Generator extension will be documented in this file.

## [1.0.0] - 2023-08-10

### Added
- Initial release of the Screenshot Comment Generator extension
- Region selection with Lightshot-style rectangle drawing
- Draggable and resizable selection rectangle
- Screenshot capture using chrome.tabs.captureVisibleTab()
- Screenshot cropping based on selection coordinates
- Popup UI with three screens: capture, preview, and result
- Caption input for providing context to the AI
- Comment generation via Python backend
- Copy, edit, and regenerate comment functionality
- Loading and error handling
- Notification system

### Security
- HTTPS-only communication with backend
- Minimal permissions required
- No permanent storage of user data

## [0.1.0] - 2023-07-15

### Added
- Initial prototype with basic screenshot functionality
- Proof of concept for selection rectangle
- Simple API integration 