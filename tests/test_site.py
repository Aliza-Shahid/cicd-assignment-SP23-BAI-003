import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

APP_URL = os.getenv("APP_URL", "http://host.docker.internal:8081")
REPORT_DIR = "/app/reports"

@pytest.fixture(scope="module")
def driver():
    os.makedirs(REPORT_DIR, exist_ok=True)
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,800")

    service = Service("/usr/bin/chromedriver")
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.implicitly_wait(5)
    yield browser
    browser.quit()

def test_01_page_title(driver):
    driver.get(APP_URL)
    assert "SP23-BAI-003" in driver.title

def test_02_heading_contains_name_and_roll(driver):
    driver.get(APP_URL)
    heading = driver.find_element(By.ID, "student-heading").text
    assert "Aliza Shahid" in heading
    assert "SP23-BAI-003" in heading

def test_03_button_click_displays_message(driver):
    driver.get(APP_URL)
    btn = driver.find_element(By.ID, "greet-btn")
    btn.click()
    output = driver.find_element(By.ID, "greet-output").text
    assert "Hello Aliza! CI/CD Pipeline Verified." in output

def test_04_textbox_submit_and_screenshot(driver):
    driver.get(APP_URL)
    text_box = driver.find_element(By.ID, "user-input")
    text_box.clear()
    text_box.send_keys("Automated Selenium Verification")
    driver.find_element(By.ID, "submit-btn").click()

    submitted = driver.find_element(By.ID, "submitted-output").text
    assert "Submitted: Automated Selenium Verification" in submitted

    driver.save_screenshot(os.path.join(REPORT_DIR, "selenium_test_proof.png"))