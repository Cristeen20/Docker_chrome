from flask import Flask, jsonify, request
import asyncio
from pyppeteer import launch

app = Flask(__name__)

# Function to capture screenshot using Pyppeteer
async def capture_screenshot(url):
    browser = await launch(handleSIGINT=False,
                        handleSIGTERM=False,
                        handleSIGHUP=True,
                        headless=True)
    page = await browser.newPage()
    await page.goto(url)
    screenshot_path = 'screenshot.png'
    await page.screenshot({'path': screenshot_path})
    await browser.close()
    return screenshot_path

@app.route('/', methods=['POST','GET'])
def load():
    return "docker trials"

# API endpoint to take a screenshot
@app.route('/screenshot', methods=['POST','GET'])
def screenshot():
    try:
        url = 'https://www.tripadvisor.ca/AITripBuilder'
        if not url:
            return jsonify({"error": "URL is required"}), 400

        # Launch Pyppeteer and capture screenshot
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:  # If there is no event loop in the current thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Launch Pyppeteer and capture screenshot
        screenshot_path = loop.run_until_complete(capture_screenshot(url))
        
        return jsonify({"screenshot_path": screenshot_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
