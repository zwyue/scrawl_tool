from selenium.webdriver.chrome.options import Options
import os

def get_options():
    options = Options()

    user_data_dir = os.environ.get("CHROME_USER_DATA_DIR")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-data-dir=" + user_data_dir)
    options.add_argument("--incognito")
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")
    return options