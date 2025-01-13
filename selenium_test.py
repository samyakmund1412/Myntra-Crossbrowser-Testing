import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService

def setup_driver(browser_name):
    """Set up the WebDriver for the specified browser."""
    if browser_name.lower() == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_service = ChromeService(ChromeDriverManager().install())  # Setup driver using Service
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    elif browser_name.lower() == "edge":
        edge_options = EdgeOptions()
        edge_options.add_argument("--start-maximized")
        edge_service = EdgeService(EdgeChromiumDriverManager().install())  # Setup driver using Service
        driver = webdriver.Edge(service=edge_service, options=edge_options)
    else:
        raise ValueError("Unsupported browser. Use 'chrome' or 'edge'.")
    return driver

def open_homepage(driver, browser_name):
    driver.get("https://www.myntra.com")
    print(f"Opened Myntra homepage using {browser_name.capitalize()}.")

def search_product(driver, browser_name, product_name):
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@class="desktop-searchBar"]'))
    )
    search_box.send_keys(product_name)
    search_box.send_keys(Keys.RETURN)
    print(f"Searched for '{product_name}' using {browser_name.capitalize()}.")

def click_first_product(driver, browser_name):
    first_product = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@class="product-base"]'))
    )
    first_product.click()
    print(f"Clicked on the first product using {browser_name.capitalize()}.")

def add_to_cart(driver, browser_name):
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="ADD TO BAG"]'))
    )
    add_to_cart_button.click()
    print(f"Added product to the cart using {browser_name.capitalize()}.")

def navigate_to_cart(driver, browser_name):
    cart_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@href="/shop/cart"]'))
    )
    cart_icon.click()
    print(f"Navigated to the cart using {browser_name.capitalize()}.")

def verify_product_in_cart(driver, browser_name, product_name):
    cart_product = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="itemContainer-base-info"]'))
    )
    assert product_name.lower() in cart_product.text.lower(), f"Product '{product_name}' not found in cart!"
    print(f"Product verification successful using {browser_name.capitalize()}.")

def perform_task_in_browser(browser_name, product_name):
    try:
        driver = setup_driver(browser_name)
        if not driver:
            return

        open_homepage(driver, browser_name)
        search_product(driver, browser_name, product_name)
        click_first_product(driver, browser_name)
        add_to_cart(driver, browser_name)
        navigate_to_cart(driver, browser_name)
        verify_product_in_cart(driver, browser_name, product_name)

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Test Failed on {browser_name.capitalize()} - {e}")
    except AssertionError as ae:
        print(f"Verification Error on {browser_name.capitalize()} - {ae}")
    except Exception as ex:
        print(f"Unexpected error in {browser_name.capitalize()}: {ex}")
    finally:
        if 'driver' in locals() and driver:
            driver.quit()
            print(f"{browser_name.capitalize()} Browser closed.")

# Threads for each browser
chrome_thread = threading.Thread(target=perform_task_in_browser, args=("chrome", "Shirt"))
edge_thread = threading.Thread(target=perform_task_in_browser, args=("edge", "Shirt"))

# Start both threads
chrome_thread.start()
edge_thread.start()

# Wait for threads to complete
chrome_thread.join()
edge_thread.join()

print("Cross-browser testing completed.")
