from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager

ACCOUNT_EMAIL = 'YOUR LOGIN EMAIL'
ACCOUNT_PASSWORD = 'YOUR LOGIN PASSWORD'
PHONE = 'YOUR PHONE NUMBER'


def find_and_click_element(by, value):
    element = driver.find_element(by=by, value=value)
    element.click()
    return element


def find_and_send_keys(by, value, keys):
    element = driver.find_element(by=by, value=value)
    element.send_keys(keys)
    return element


def abort_application():
    find_and_click_element(By.CLASS_NAME, "artdeco-modal__dismiss")
    time.sleep(2)
    discard_buttons = driver.find_elements(By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn")
    discard_buttons[1].click()


chrome_driver_path = 'YOUR CHROME DRIVER PATH'
chrome_driver_path = ChromeDriverManager(path='YOUR CHROME DRIVER FOLDER').install()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3586148395&f_LF=f_AL&geoId=101356765&"
           "keywords=python&location=London%2C%20England%2C%20United%20Kingdom&refresh=true")

time.sleep(2)
find_and_click_element(By.CSS_SELECTOR, 'button[action-type="DENY"]')

time.sleep(2)
find_and_click_element(By.LINK_TEXT, "Sign in")

time.sleep(5)
find_and_send_keys(By.ID, "username", ACCOUNT_EMAIL)
find_and_send_keys(By.ID, "password", ACCOUNT_PASSWORD).send_keys(Keys.ENTER)

input("Press Enter when you have solved the Captcha")

time.sleep(5)
all_listings = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")

for listing in all_listings:
    print("Opening Listing")
    listing.click()
    time.sleep(2)

    try:
        find_and_click_element(By.CSS_SELECTOR, ".jobs-s-apply button")
        time.sleep(5)

        phone = find_and_send_keys(By.CSS_SELECTOR, "input[id*=phoneNumber]", PHONE)

        submit_button = driver.find_element(By.CSS_SELECTOR, "footer button")

        if submit_button.get_attribute("data-control-name") == "continue_unify":
            abort_application()
            print("Complex application, skipped.")
            continue
        else:
            print("Submitting job application")
            submit_button.click()

        time.sleep(2)
        find_and_click_element(By.CLASS_NAME, "artdeco-modal__dismiss")

    except NoSuchElementException:
        abort_application()
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()