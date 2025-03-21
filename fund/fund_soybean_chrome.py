import json
import time

from selenium import webdriver

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Optional: Run headless if you don't need a UI
chrome_options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})

chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Set up WebDriver with ChromeDriverManager
# service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=chrome_options)

# Enable Network events in the DevTools Protocol
driver.execute_cdp_cmd("Network.enable", {})


# Callback to handle network request events
def capture_network_request(request):
    # Print network request details
    print(f"Request URL: {request['request']['url']}")
    print(f"Request Method: {request['request']['method']}")
    print(f"Request Headers: {json.dumps(request['request']['headers'], indent=2)}")


# Hook up to network events (captures network traffic)
driver.request_interceptor = capture_network_request

# Open the website
driver.get('http://www.dce.com.cn/dalianshangpin/sspz/487180/index.html')

# Allow time for network requests to be captured
time.sleep(5)

# Close the driver
driver.quit()
