from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config import CHROME_BINARY_PATH, CHROMEDRIVER_PATH

# Configure options
options = Options()
options.binary_location = CHROME_BINARY_PATH
options.add_argument("--headless")  # Optional: run without GUI
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Start driver
driver = webdriver.Chrome(
    service=Service(CHROMEDRIVER_PATH),
    options=options
)

# Test: open Bilibili search
driver.get("https://search.bilibili.com/all?keyword=科技")
print("✅ Page Title:", driver.title)

# (Optional) Show length of page HTML
print("✅ HTML Length:", len(driver.page_source))

# Done
driver.quit()
