/**
 * Utility functions for the Screenshot Comment Generator extension
 */

// Format a timestamp as a readable string
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

// Copy text to clipboard
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (error) {
        console.error('Failed to copy text:', error);
        return false;
    }
}

// Validate that the image is a valid base64 string
function validateBase64Image(base64String) {
    if (!base64String) return false;

    // Check if it's a valid base64 data URL
    const regex = /^data:image\/(png|jpeg|jpg|gif);base64,/;
    if (!regex.test(base64String)) return false;

    // Remove the data URL prefix to get the base64 string
    const base64 = base64String.split(',')[1];

    // Check if it's a valid base64 string
    try {
        return btoa(atob(base64)) === base64;
    } catch (error) {
        console.error('Invalid base64 string:', error);
        return false;
    }
}

// Show a notification to the user
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Auto-remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 500);
    }, 3000);
}

// Export the functions
window.utils = {
    formatTimestamp,
    copyToClipboard,
    validateBase64Image,
    showNotification
};
