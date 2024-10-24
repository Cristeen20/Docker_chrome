from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# Function to capture screenshot using Selenium
def capture_screenshot(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")  # Overcome limited resource problems
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Set up the WebDriver (using Chrome)
    CHROME_PATH = "chromedriver-linux64\chromedriver"
    driver = webdriver.Chrome(service=Service(CHROME_PATH), options=chrome_options)

    # Navigate to the URL and take a screenshot
    driver.get(url)
    screenshot_path = 'screenshot.png'
    driver.save_screenshot(screenshot_path)
    driver.quit()
    
    return screenshot_path

@app.route('/', methods=['POST', 'GET'])
def load():
    return "docker trials"

# API endpoint to take a screenshot
@app.route('/screenshot', methods=['POST', 'GET'])
def screenshot():
    try:
        url = 'https://www.tripadvisor.ca/AITripBuilder'
        if not url:
            return jsonify({"error": "URL is required"}), 400

        # Capture screenshot
        try:
            screenshot_path = capture_screenshot(url)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        return jsonify({"screenshot_path": screenshot_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
