// Selection Rectangle Tests

const assert = require('assert');
const puppeteer = require('puppeteer');

describe('Selection Rectangle', function () {
    let browser;
    let page;

    before(async function () {
        this.timeout(10000);
        browser = await puppeteer.launch({
            headless: false,
            args: [
                '--disable-extensions-except=../chrome-extension',
                '--load-extension=../chrome-extension'
            ]
        });
        page = await browser.newPage();
    });

    after(async function () {
        await browser.close();
    });

    it('should create a selection rectangle on mousedown and move', async function () {
        await page.goto('https://example.com');

        // Inject the content script
        await page.evaluate(() => {
            const script = document.createElement('script');
            script.src = chrome.runtime.getURL('js/content.js');
            document.head.appendChild(script);
        });

        // Simulate mousedown event
        await page.mouse.move(100, 100);
        await page.mouse.down();

        // Check if the selection box is created
        const selectionBox = await page.$('#screenshot-selection-box');
        assert.ok(selectionBox, 'Selection box should be created on mousedown');

        // Simulate mouse move to create a rectangle
        await page.mouse.move(200, 200);

        // Check the dimensions of the selection box
        const dimensions = await page.evaluate(() => {
            const box = document.getElementById('screenshot-selection-box');
            return {
                left: parseInt(box.style.left),
                top: parseInt(box.style.top),
                width: parseInt(box.style.width),
                height: parseInt(box.style.height)
            };
        });

        assert.equal(dimensions.left, 100, 'Selection box should start at x=100');
        assert.equal(dimensions.top, 100, 'Selection box should start at y=100');
        assert.equal(dimensions.width, 100, 'Selection box should have width=100');
        assert.equal(dimensions.height, 100, 'Selection box should have height=100');
    });

    it('should allow resizing the selection rectangle', async function () {
        // Create a selection first
        await page.mouse.move(100, 100);
        await page.mouse.down();
        await page.mouse.move(200, 200);
        await page.mouse.up();

        // Find the southeast resize handle
        const seHandle = await page.$('.resize-handle.se');

        // Get the position of the handle
        const handlePos = await page.evaluate(handle => {
            const rect = handle.getBoundingClientRect();
            return {
                x: rect.left + rect.width / 2,
                y: rect.top + rect.height / 2
            };
        }, seHandle);

        // Drag the handle to resize
        await page.mouse.move(handlePos.x, handlePos.y);
        await page.mouse.down();
        await page.mouse.move(300, 300);
        await page.mouse.up();

        // Check the new dimensions
        const newDimensions = await page.evaluate(() => {
            const box = document.getElementById('screenshot-selection-box');
            return {
                width: parseInt(box.style.width),
                height: parseInt(box.style.height)
            };
        });

        assert.equal(newDimensions.width, 200, 'Selection box should have width=200 after resize');
        assert.equal(newDimensions.height, 200, 'Selection box should have height=200 after resize');
    });

    it('should allow dragging the selection rectangle', async function () {
        // Create a selection first
        await page.mouse.move(100, 100);
        await page.mouse.down();
        await page.mouse.move(200, 200);
        await page.mouse.up();

        // Find the center of the selection box
        const center = await page.evaluate(() => {
            const box = document.getElementById('screenshot-selection-box');
            const rect = box.getBoundingClientRect();
            return {
                x: rect.left + rect.width / 2,
                y: rect.top + rect.height / 2
            };
        });

        // Drag the selection box
        await page.mouse.move(center.x, center.y);
        await page.mouse.down();
        await page.mouse.move(center.x + 50, center.y + 50);
        await page.mouse.up();

        // Check the new position
        const newPosition = await page.evaluate(() => {
            const box = document.getElementById('screenshot-selection-box');
            return {
                left: parseInt(box.style.left),
                top: parseInt(box.style.top)
            };
        });

        assert.equal(newPosition.left, 150, 'Selection box should be moved to x=150');
        assert.equal(newPosition.top, 150, 'Selection box should be moved to y=150');
    });
}); 