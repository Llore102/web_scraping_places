from selenium import webdriver
import time


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Remote(
        command_executor='http://localhost:4444',
        options=options
    )


    return driver

def get_driver_with_retry(retries=3, delay=15):  # Aumenta el tiempo de espera a 5m
    for _ in range(retries):
        try:
            driver = get_driver()
            return driver
        except Exception as e:
            print(f"Error creating WebDriver: {e}")
            print("Retrying...")
            time.sleep(delay)
    raise Exception("Failed to create WebDriver after multiple retries.")
