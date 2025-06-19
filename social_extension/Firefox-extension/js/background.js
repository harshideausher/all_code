// Background script for handling screenshot capture

// This function crops a base64 image based on the given coordinates
async function cropImage(base64Image, cropData) {
    return new Promise(async (resolve, reject) => {
        try {
            // Create an image element to load the base64 image
            const img = new Image();
            img.onload = function () {
                // Get the device pixel ratio or use the one passed in cropData
                const scale = cropData.scale || 1;

                // Adjust coordinates based on the scale if needed
                const x = cropData.x / scale;
                const y = cropData.y / scale;
                const width = cropData.width / scale;
                const height = cropData.height / scale;

                // Create a canvas with target dimensions
                const canvas = document.createElement('canvas');
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');

                // Draw the portion of the image we want to keep
                ctx.drawImage(
                    img,
                    x, y, width, height,
                    0, 0, width, height
                );

                // Convert the canvas to a base64 encoded PNG
                resolve(canvas.toDataURL('image/png'));
            };

            img.onerror = function () {
                reject(new Error('Failed to load image'));
            };

            img.src = base64Image;
        } catch (error) {
            reject(error);
        }
    });
}

// Ensure the content script is loaded and then send a message
function ensureContentScriptAndSendMessage(tabId, message, callback) {
    try {
        // First, try to send a message directly
        browser.tabs.sendMessage(tabId, { action: 'ping' }).then(
            response => {
                // Content script is already loaded, send the actual message
                browser.tabs.sendMessage(tabId, message).then(callback, error => {
                    console.error('Error sending message:', error);
                    callback({ success: false, error: error.message });
                });
            },
            error => {
                // Content script isn't loaded, inject it
                browser.tabs.executeScript(tabId, {
                    file: 'js/content.js'
                }).then(() => {
                    // Give it a moment to initialize
                    setTimeout(() => {
                        // Now send the actual message
                        browser.tabs.sendMessage(tabId, message).then(callback, error => {
                            console.error('Error sending message after injection:', error);
                            callback({ success: false, error: error.message });
                        });
                    }, 100);
                }).catch(error => {
                    console.error('Error injecting content script:', error);
                    callback({ success: false, error: 'Failed to inject content script: ' + error.message });
                });
            }
        );
    } catch (error) {
        console.error('Error in ensureContentScriptAndSendMessage:', error);
        callback({ success: false, error: error.message });
    }
}

// Handle messages from content script or popup
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'initiateCapture') {
        // Notify content script to start selection mode
        browser.tabs.query({ active: true, currentWindow: true }).then(tabs => {
            if (tabs[0]) {
                ensureContentScriptAndSendMessage(
                    tabs[0].id,
                    { action: 'startSelection' },
                    (response) => {
                        if (response && response.success) {
                            sendResponse({ success: true });
                        } else {
                            sendResponse({ success: false, error: 'Could not start selection' });
                        }
                    }
                );
            } else {
                sendResponse({ success: false, error: 'No active tab found' });
            }
        }).catch(error => {
            console.error('Error querying tabs:', error);
            sendResponse({ success: false, error: error.message });
        });
        return true; // Keep the message channel open for the async response
    }

    else if (message.action === 'captureRegion') {
        const captureData = message.data;

        // Capture the visible tab
        browser.tabs.captureVisibleTab({ format: 'png' }).then(async screenshotUrl => {
            try {
                // Crop the screenshot to the selected region
                const croppedImage = await cropImage(screenshotUrl, captureData);

                // Store the image in browser.storage for the popup to access
                browser.storage.local.set({
                    capturedImage: croppedImage,
                    captureTime: Date.now()
                }).then(() => {
                    // Open the popup for the user to see the result
                    browser.browserAction.openPopup();
                    sendResponse({ success: true });
                }).catch(error => {
                    console.error('Error storing image:', error);
                    sendResponse({ success: false, error: error.message });
                });
            } catch (error) {
                console.error('Error processing screenshot:', error);
                sendResponse({ success: false, error: error.message });
            }
        }).catch(error => {
            console.error('Error capturing tab:', error);
            sendResponse({ success: false, error: error.message });
        });

        return true; // Keep the message channel open for the async response
    }

    else if (message.action === 'generateComment') {
        const apiData = {
            image: message.imageData,
            caption: message.caption || ''
        };

        console.log('Preparing to send comment request to server');

        // Updated API endpoint to point to local Flask server
        const apiEndpoint = 'http://localhost:8000/generate-comment';

        // Call the API to generate a comment with improved error handling
        try {
            fetch(apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                mode: 'cors', // Explicitly set CORS mode
                cache: 'no-cache', // Don't use cache
                body: JSON.stringify(apiData)
            })
                .then(response => {
                    console.log('Server response status:', response.status);
                    if (!response.ok) {
                        return response.text().then(text => {
                            console.error('Server error response:', text);
                            throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Received comment data from server');
                    sendResponse({ success: true, comment: data.comment });
                })
                .catch(error => {
                    console.error('Error in fetch operation:', error);
                    // More descriptive error message
                    let errorMessage = error.message;
                    if (errorMessage.includes('Failed to fetch')) {
                        errorMessage = 'Could not connect to the Python server. Make sure comment_generator.py is running on http://localhost:8000';
                    }
                    sendResponse({ success: false, error: errorMessage });
                });
        } catch (error) {
            console.error('Exception before fetch:', error);
            sendResponse({ success: false, error: 'Error preparing request: ' + error.message });
        }

        return true; // Keep the message channel open for the async response
    }

    // Firefox requires a return true to use sendResponse asynchronously
    return true;
});



