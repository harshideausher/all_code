(() => {
    let isSelecting = false;
    let startX = 0;
    let startY = 0;
    let endX = 0;
    let endY = 0;
    let selectionBox = null;
    let isDragging = false;
    let dragStartX = 0;
    let dragStartY = 0;
    let dragOffsetX = 0;
    let dragOffsetY = 0;
    let isResizing = false;
    let currentResizeHandle = null;

    function createSelectionBox() {
        // Create the selection box if it doesn't exist
        if (!selectionBox) {
            selectionBox = document.createElement('div');
            selectionBox.id = 'screenshot-selection-box';
            selectionBox.style.position = 'fixed';
            selectionBox.style.border = '2px dashed #1a73e8';
            selectionBox.style.backgroundColor = 'rgba(26, 115, 232, 0.1)';
            selectionBox.style.zIndex = '2147483647';
            selectionBox.style.cursor = 'move';
            selectionBox.style.display = 'none';

            // Add resize handles
            const positions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'];
            positions.forEach(pos => {
                const handle = document.createElement('div');
                handle.className = `resize-handle ${pos}`;
                handle.dataset.position = pos;
                handle.style.position = 'absolute';
                handle.style.width = '10px';
                handle.style.height = '10px';
                handle.style.backgroundColor = '#ffffff';
                handle.style.border = '1px solid #1a73e8';

                // Position the handles
                switch (pos) {
                    case 'n':
                        handle.style.top = '-5px';
                        handle.style.left = 'calc(50% - 5px)';
                        handle.style.cursor = 'n-resize';
                        break;
                    case 'ne':
                        handle.style.top = '-5px';
                        handle.style.right = '-5px';
                        handle.style.cursor = 'ne-resize';
                        break;
                    case 'e':
                        handle.style.top = 'calc(50% - 5px)';
                        handle.style.right = '-5px';
                        handle.style.cursor = 'e-resize';
                        break;
                    case 'se':
                        handle.style.bottom = '-5px';
                        handle.style.right = '-5px';
                        handle.style.cursor = 'se-resize';
                        break;
                    case 's':
                        handle.style.bottom = '-5px';
                        handle.style.left = 'calc(50% - 5px)';
                        handle.style.cursor = 's-resize';
                        break;
                    case 'sw':
                        handle.style.bottom = '-5px';
                        handle.style.left = '-5px';
                        handle.style.cursor = 'sw-resize';
                        break;
                    case 'w':
                        handle.style.top = 'calc(50% - 5px)';
                        handle.style.left = '-5px';
                        handle.style.cursor = 'w-resize';
                        break;
                    case 'nw':
                        handle.style.top = '-5px';
                        handle.style.left = '-5px';
                        handle.style.cursor = 'nw-resize';
                        break;
                }

                selectionBox.appendChild(handle);
            });

            // Add buttons
            const buttonsContainer = document.createElement('div');
            buttonsContainer.className = 'selection-buttons';
            buttonsContainer.style.position = 'absolute';
            buttonsContainer.style.top = '-30px';
            buttonsContainer.style.right = '0';

            const captureButton = document.createElement('button');
            captureButton.textContent = 'Capture';
            captureButton.style.backgroundColor = '#1a73e8';
            captureButton.style.color = '#ffffff';
            captureButton.style.border = 'none';
            captureButton.style.borderRadius = '4px';
            captureButton.style.padding = '5px 10px';
            captureButton.style.marginRight = '5px';
            captureButton.style.cursor = 'pointer';

            const cancelButton = document.createElement('button');
            cancelButton.textContent = 'Cancel';
            cancelButton.style.backgroundColor = '#f1f3f4';
            cancelButton.style.color = '#202124';
            cancelButton.style.border = 'none';
            cancelButton.style.borderRadius = '4px';
            cancelButton.style.padding = '5px 10px';
            cancelButton.style.cursor = 'pointer';

            // Button event listeners
            captureButton.addEventListener('click', handleCapture);
            cancelButton.addEventListener('click', handleCancel);

            buttonsContainer.appendChild(captureButton);
            buttonsContainer.appendChild(cancelButton);
            selectionBox.appendChild(buttonsContainer);

            document.body.appendChild(selectionBox);
        }
        return selectionBox;
    }

    function updateSelectionBox() {
        if (!selectionBox) return;

        const left = Math.min(startX, endX);
        const top = Math.min(startY, endY);
        const width = Math.abs(endX - startX);
        const height = Math.abs(endY - startY);

        selectionBox.style.left = `${left}px`;
        selectionBox.style.top = `${top}px`;
        selectionBox.style.width = `${width}px`;
        selectionBox.style.height = `${height}px`;
    }

    function handleCapture() {
        if (!selectionBox) return;

        const rect = selectionBox.getBoundingClientRect();
        const captureData = {
            x: rect.left,
            y: rect.top,
            width: rect.width,
            height: rect.height
        };

        // Send message to background script to capture screenshot
        chrome.runtime.sendMessage({
            action: 'captureRegion',
            data: captureData
        });

        // Clean up
        resetSelection();
    }

    function handleCancel() {
        resetSelection();
    }

    function resetSelection() {
        if (selectionBox) {
            document.body.removeChild(selectionBox);
            selectionBox = null;
        }
        isSelecting = false;
        isDragging = false;
        isResizing = false;
    }

    function onMouseDown(e) {
        if (selectionBox && selectionBox.contains(e.target)) {
            // Check if clicking on a resize handle
            if (e.target.classList.contains('resize-handle')) {
                isResizing = true;
                currentResizeHandle = e.target.dataset.position;
                e.preventDefault();
                return;
            }

            // Handle dragging the selection box
            isDragging = true;
            dragStartX = e.clientX;
            dragStartY = e.clientY;
            const rect = selectionBox.getBoundingClientRect();
            dragOffsetX = dragStartX - rect.left;
            dragOffsetY = dragStartY - rect.top;
            e.preventDefault();
            return;
        }

        // Start a new selection
        isSelecting = true;
        startX = e.clientX;
        startY = e.clientY;
        endX = startX;
        endY = startY;

        // Create and show the selection box
        selectionBox = createSelectionBox();
        selectionBox.style.display = 'block';
        updateSelectionBox();
    }

    function onMouseMove(e) {
        if (isResizing && selectionBox) {
            // Handle resizing
            const rect = selectionBox.getBoundingClientRect();

            switch (currentResizeHandle) {
                case 'n':
                    startY = e.clientY;
                    break;
                case 'ne':
                    startY = e.clientY;
                    endX = e.clientX;
                    break;
                case 'e':
                    endX = e.clientX;
                    break;
                case 'se':
                    endY = e.clientY;
                    endX = e.clientX;
                    break;
                case 's':
                    endY = e.clientY;
                    break;
                case 'sw':
                    endY = e.clientY;
                    startX = e.clientX;
                    break;
                case 'w':
                    startX = e.clientX;
                    break;
                case 'nw':
                    startY = e.clientY;
                    startX = e.clientX;
                    break;
            }

            updateSelectionBox();
        } else if (isDragging && selectionBox) {
            // Handle dragging
            const newLeft = e.clientX - dragOffsetX;
            const newTop = e.clientY - dragOffsetY;

            // Update start and end coordinates
            const width = Math.abs(endX - startX);
            const height = Math.abs(endY - startY);

            startX = newLeft;
            startY = newTop;
            endX = startX + width;
            endY = startY + height;

            updateSelectionBox();
        } else if (isSelecting) {
            // Handle drawing the selection
            endX = e.clientX;
            endY = e.clientY;
            updateSelectionBox();
        }
    }

    function onMouseUp(e) {
        if (isSelecting) {
            // Finish selection
            endX = e.clientX;
            endY = e.clientY;
            updateSelectionBox();

            // If selection is too small, reset
            const width = Math.abs(endX - startX);
            const height = Math.abs(endY - startY);
            if (width < 10 && height < 10) {
                resetSelection();
            }
        }

        isSelecting = false;
        isDragging = false;
        isResizing = false;
    }

    // Listen for messages from background script
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.action === 'ping') {
            // Respond to ping to indicate content script is loaded
            sendResponse({ success: true });
        } else if (message.action === 'startSelection') {
            // Activate selection mode
            document.addEventListener('mousedown', onMouseDown);
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
            sendResponse({ success: true });
        } else if (message.action === 'cancelSelection') {
            resetSelection();
            document.removeEventListener('mousedown', onMouseDown);
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
            sendResponse({ success: true });
        }
        return true;
    });
})();
