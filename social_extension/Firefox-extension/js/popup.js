// Popup JavaScript

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const captureScreen = document.getElementById('capture-screen');
    const previewScreen = document.getElementById('preview-screen');
    const resultScreen = document.getElementById('result-screen');

    const captureBtn = document.getElementById('capture-btn');
    const screenshotPreview = document.getElementById('screenshot-preview');
    const captureTime = document.getElementById('capture-time');
    const captionInput = document.getElementById('caption-input');
    const generateBtn = document.getElementById('generate-btn');
    const recaptureBtn = document.getElementById('recapture-btn');

    const resultScreenshot = document.getElementById('result-screenshot');
    const commentDisplay = document.getElementById('comment-display');
    const copyBtn = document.getElementById('copy-btn');
    const editBtn = document.getElementById('edit-btn');
    const regenerateBtn = document.getElementById('regenerate-btn');
    const startOverBtn = document.getElementById('start-over-btn');

    const editCommentContainer = document.getElementById('edit-comment-container');
    const editCommentInput = document.getElementById('edit-comment-input');
    const saveEditBtn = document.getElementById('save-edit-btn');
    const cancelEditBtn = document.getElementById('cancel-edit-btn');

    const loadingOverlay = document.getElementById('loading-overlay');
    const loadingMessage = document.getElementById('loading-message');
    const errorMessage = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    const errorDismissBtn = document.getElementById('error-dismiss-btn');

    // State
    let currentCapturedImage = null;
    let currentGeneratedComment = null;

    // Check if we have a captured image in storage
    browser.storage.local.get(['capturedImage', 'captureTime']).then(result => {
        if (result.capturedImage) {
            currentCapturedImage = result.capturedImage;
            showPreviewScreen(result.capturedImage, result.captureTime);
        }
    }).catch(error => {
        console.error('Error getting from storage:', error);
    });

    // Event listeners
    captureBtn.addEventListener('click', startCapture);
    generateBtn.addEventListener('click', generateComment);
    recaptureBtn.addEventListener('click', resetToCapture);

    copyBtn.addEventListener('click', copyComment);
    editBtn.addEventListener('click', showEditComment);
    regenerateBtn.addEventListener('click', regenerateComment);
    startOverBtn.addEventListener('click', resetToCapture);

    saveEditBtn.addEventListener('click', saveEditedComment);
    cancelEditBtn.addEventListener('click', cancelEditComment);

    errorDismissBtn.addEventListener('click', dismissError);

    // Functions
    function startCapture() {
        showLoading('Preparing capture tool...');

        // Send message to the background script to initiate capture
        browser.runtime.sendMessage({ action: 'initiateCapture' }).then(response => {
            hideLoading();

            if (response && response.success) {
                // Close the popup to allow the user to select a region
                window.close();
            } else {
                showError('Failed to start screen capture. Please try again.');
            }
        }).catch(error => {
            hideLoading();
            showError('Error: ' + error.message);
        });
    }

    function showPreviewScreen(imageData, timestamp) {
        // Show the preview screen
        captureScreen.classList.remove('active');
        previewScreen.classList.add('active');
        resultScreen.classList.remove('active');

        // Set the preview image
        screenshotPreview.src = imageData;

        // Set the capture time
        if (timestamp) {
            captureTime.textContent = window.utils.formatTimestamp(timestamp);
        }
    }

    function generateComment() {
        // Get the caption from the input
        const caption = captionInput.value.trim();

        // Validate the image
        if (!currentCapturedImage) {
            showError('No image captured. Please capture an image first.');
            return;
        }

        showLoading('Generating comment...');

        // Send message to the background script to generate a comment
        browser.runtime.sendMessage({
            action: 'generateComment',
            imageData: currentCapturedImage,
            caption: caption
        }).then(response => {
            hideLoading();

            if (response && response.success) {
                currentGeneratedComment = response.comment;
                showResultScreen(currentCapturedImage, response.comment);
            } else {
                showError('Failed to generate comment: ' + (response?.error || 'Unknown error'));
            }
        }).catch(error => {
            hideLoading();
            showError('Error: ' + error.message);
        });
    }

    function showResultScreen(imageData, comment) {
        // Show the result screen
        captureScreen.classList.remove('active');
        previewScreen.classList.remove('active');
        resultScreen.classList.add('active');

        // Set the result image
        resultScreenshot.src = imageData;

        // Set the comment
        commentDisplay.textContent = comment;
    }

    function resetToCapture() {
        // Reset to the capture screen
        captureScreen.classList.add('active');
        previewScreen.classList.remove('active');
        resultScreen.classList.remove('active');

        // Reset state
        currentCapturedImage = null;
        currentGeneratedComment = null;
        captionInput.value = '';

        // Clear storage
        browser.storage.local.remove(['capturedImage', 'captureTime']);
    }

    function copyComment() {
        if (!currentGeneratedComment) return;

        window.utils.copyToClipboard(currentGeneratedComment)
            .then(success => {
                if (success) {
                    window.utils.showNotification('Comment copied to clipboard!', 'success');
                } else {
                    window.utils.showNotification('Failed to copy comment.', 'error');
                }
            });
    }

    function showEditComment() {
        editCommentInput.value = currentGeneratedComment || '';
        editCommentContainer.classList.remove('hidden');
    }

    function saveEditedComment() {
        const editedComment = editCommentInput.value.trim();
        if (editedComment) {
            currentGeneratedComment = editedComment;
            commentDisplay.textContent = editedComment;
            editCommentContainer.classList.add('hidden');
        }
    }

    function cancelEditComment() {
        editCommentContainer.classList.add('hidden');
    }

    function regenerateComment() {
        // Get the caption from the input (in case it was changed)
        const caption = captionInput.value.trim();

        showLoading('Regenerating comment...');

        // Send message to the background script to generate a new comment
        browser.runtime.sendMessage({
            action: 'generateComment',
            imageData: currentCapturedImage,
            caption: caption
        }).then(response => {
            hideLoading();

            if (response && response.success) {
                currentGeneratedComment = response.comment;
                commentDisplay.textContent = response.comment;
            } else {
                showError('Failed to regenerate comment: ' + (response?.error || 'Unknown error'));
            }
        }).catch(error => {
            hideLoading();
            showError('Error: ' + error.message);
        });
    }

    function showLoading(message) {
        loadingMessage.textContent = message || 'Loading...';
        loadingOverlay.classList.remove('hidden');
    }

    function hideLoading() {
        loadingOverlay.classList.add('hidden');
    }

    function showError(message) {
        errorText.textContent = message;
        errorMessage.classList.remove('hidden');
    }

    function dismissError() {
        errorMessage.classList.add('hidden');
    }
});
