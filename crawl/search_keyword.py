import pickle
import re
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("user-data-dir=C:/Users/DNV/AppData/Local/Google/Chrome/User Data")
options.add_argument("profile-directory=Default")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Load cookies if available
cookies_loaded = False
try:
    with open("cookies.pkl", "rb") as file:
        cookies = pickle.load(file)
        driver.get("https://shopee.vn")
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        cookies_loaded = True
except FileNotFoundError:
    print("Cookies file not found. Proceeding without loading cookies.")

# Navigate to Shopee if cookies were not loaded
if not cookies_loaded:
    driver.get("https://shopee.vn")
# Wait for the page to load
wait = WebDriverWait(driver, 20)

try:
    # Check if the user is already logged in by looking for the user profile element
    user_profile = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.navbar__username")))
    print("Already logged in")
    cookies = driver.get_cookies()
    with open("cookies.pkl", "wb") as file:
        pickle.dump(cookies, file)
except TimeoutException:
    print("Not logged in, proceeding with login")
    
    # Navigate to the login page
    driver.get("https://shopee.vn/")

    # Wait for the login form to be visible
    login_key = wait.until(EC.visibility_of_element_located((By.NAME, "loginKey")))
    password = wait.until(EC.visibility_of_element_located((By.NAME, "password")))

    # Clear the text fields
    login_key.clear()
    password.clear()

    # Add random delay to mimic human behavior
    time.sleep(random.uniform(1, 3))

    # Fill in the login form
    login_key.send_keys("0389120457")
    time.sleep(random.uniform(1, 3))
    password.send_keys("Vypro123")

    # Click the login button
    login_button = driver.find_element(By.CSS_SELECTOR, "button.b5aVaf.PVSuiZ.Gqupku.qz7ctP.qxS7lQ.Q4KP5g")
    time.sleep(random.uniform(1, 3))
    login_button.click()

    # Wait for the login to complete and verify
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.navbar__username")))
        print("Login successful")
    except TimeoutException:
        print("Login failed")

# Enter product name in the search bar
search_bar = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.shopee-searchbar-input__input")))
search_bar.clear()
search_bar.send_keys("Iphone 15")  # Replace "product_name" with the actual product name
time.sleep(random.uniform(1, 3))

# Click the search button
search_button = driver.find_element(By.CSS_SELECTOR, "button.shopee-searchbar__search-button")
search_button.click()

# Wait for the search results to load
time.sleep(5)

# Find the first search result item and click on it
search_results_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.shopee-search-item-result__items li.shopee-search-item-result__item")))
if search_results_list:
    first_item = search_results_list[0]
    link = first_item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    r = re.search(r"i\.(\d+)\.(\d+)", link)
    shop_id, item_id = r[1], r[2]
    print(f"Shop ID: {shop_id}, Item ID: {item_id}")
    # first_item.click()
else:
    print("No search results found")
# Wait for 15 seconds to view the results
time.sleep(15)

driver.quit()