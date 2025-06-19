// Background service worker for handling screenshot capture

// This function crops a base64 image based on the given coordinates
async function cropImage(base64Image, cropData) {
    return new Promise(async (resolve, reject) => {
        try {
            // Convert base64 to blob
            const base64Response = await fetch(base64Image);
            const blob = await base64Response.blob();

            // Create ImageBitmap from blob (works in service workers)
            const imageBitmap = await createImageBitmap(blob);

            // Create OffscreenCanvas with target dimensions
            const canvas = new OffscreenCanvas(cropData.width, cropData.height);
            const ctx = canvas.getContext('2d');

            // Draw the portion of the image we want to keep
            ctx.drawImage(
                imageBitmap,
                cropData.x, cropData.y, cropData.width, cropData.height,
                0, 0, cropData.width, cropData.height
            );

            // Convert the canvas to a base64 encoded PNG
            const newBlob = await canvas.convertToBlob({ type: 'image/png' });

            // Convert blob to base64
            const reader = new FileReader();
            reader.onloadend = () => {
                resolve(reader.result);
            };
            reader.onerror = (error) => {
                reject(error);
            };
            reader.readAsDataURL(newBlob);
        } catch (error) {
            reject(error);
        }
    });
}

// Ensure the content script is loaded and then send a message
async function ensureContentScriptAndSendMessage(tabId, message, callback) {
    try {
        // First, try to send a message directly
        chrome.tabs.sendMessage(tabId, { action: 'ping' }, response => {
            // If there's no error, the content script is already loaded
            if (!chrome.runtime.lastError) {
                // Send the actual message
                chrome.tabs.sendMessage(tabId, message, callback);
                return;
            }

            // Content script isn't loaded, inject it
            chrome.scripting.executeScript({
                target: { tabId: tabId },
                files: ['js/content.js']
            }, () => {
                if (chrome.runtime.lastError) {
                    console.error('Error injecting content script:', chrome.runtime.lastError);
                    callback({ success: false, error: 'Failed to inject content script' });
                    return;
                }

                // Give it a moment to initialize
                setTimeout(() => {
                    // Now send the actual message
                    chrome.tabs.sendMessage(tabId, message, callback);
                }, 100);
            });
        });
    } catch (error) {
        console.error('Error in ensureContentScriptAndSendMessage:', error);
        callback({ success: false, error: error.message });
    }
}

// Handle messages from content script or popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'initiateCapture') {
        // Notify content script to start selection mode
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (tabs[0]) {
                ensureContentScriptAndSendMessage(
                    tabs[0].id,
                    { action: 'startSelection' },
                    (response) => {
                        if (chrome.runtime.lastError) {
                            console.error('Error starting selection:', chrome.runtime.lastError);
                            sendResponse({ success: false, error: chrome.runtime.lastError.message });
                        } else if (response && response.success) {
                            sendResponse({ success: true });
                        } else {
                            sendResponse({ success: false, error: 'Could not start selection' });
                        }
                    }
                );
            } else {
                sendResponse({ success: false, error: 'No active tab found' });
            }
        });
        return true; // Keep the message channel open for the async response
    }

    else if (message.action === 'captureRegion') {
        const captureData = message.data;

        // Capture the visible tab
        chrome.tabs.captureVisibleTab({ format: 'png' }, async (screenshotUrl) => {
            try {
                // Crop the screenshot to the selected region
                const croppedImage = await cropImage(screenshotUrl, captureData);

                // Store the image in chrome.storage for the popup to access
                chrome.storage.local.set({
                    capturedImage: croppedImage,
                    captureTime: Date.now()
                }, () => {
                    // Open the popup for the user to see the result
                    chrome.action.openPopup();
                    sendResponse({ success: true });
                });
            } catch (error) {
                console.error('Error processing screenshot:', error);
                sendResponse({ success: false, error: error.message });
            }
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
});
