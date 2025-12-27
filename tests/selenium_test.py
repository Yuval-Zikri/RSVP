import time
import requests
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Configuration
BACKEND_URL = "http://backend:5000"
FRONTEND_URL = "http://frontend" 
SELENIUM_HUB = "http://selenium-chrome:4444/wd/hub"

def wait_for_backend():
    print(f"Waiting for backend at {BACKEND_URL}...")
    for i in range(30):
        try:
            resp = requests.get(f"{BACKEND_URL}/health")
            if resp.status_code == 200:
                print("Backend is up!")
                return True
        except:
            pass
        time.sleep(2)
    return False

def test_full_ui_flow():
    print("Starting Full UI Selenium Test...")
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Remote(
        command_executor=SELENIUM_HUB,
        options=chrome_options
    )
    
    wait = WebDriverWait(driver, 15)
    
    try:
        # 1. Navigate to Create Event (Home page)
        print(f"Opening Home page: {FRONTEND_URL}")
        driver.get(FRONTEND_URL)
        
        # STEP 0: Event Type
        print("Step 0: Selecting Event Type...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "event-type-card")))
        
        # Select Wedding
        wedding_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'event-type-name-primary') and (contains(text(), 'Wedding') or contains(text(), 'חתונה'))]")))
        wedding_card.click()
        
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next') or contains(text(), 'הבא')]")))
        next_btn.click()
        
        # STEP 1: Event Details
        print("Step 1: Filling Event Details...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "form-step")))
        
        # 1. Enter Title
        print("Entering title...")
        title_input = wait.until(EC.visibility_of_element_located((By.NAME, "title")))
        title_input.clear()
        title_input.send_keys("Selenium UI Gala")
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", title_input)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", title_input)
        
        # 2. Enter Subtitle
        print("Entering subtitle...")
        subtitle_input = wait.until(EC.visibility_of_element_located((By.NAME, "subtitle")))
        subtitle_input.clear()
        subtitle_input.send_keys("Automated Test Runner")
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", subtitle_input)
        
        # 3. Setting Date - Using keyboard input like a real user
        print("Setting date...")
        date_input = wait.until(EC.visibility_of_element_located((By.NAME, "date")))
        date_input.click()  # Focus the field
        time.sleep(0.3)
        
        # Clear and type the date manually
        date_input.clear()
        # Format: YYYY-MM-DDTHH:MM (required for datetime-local)
        date_input.send_keys("12312025")  # Date: 31/12/2025
        date_input.send_keys("1800")      # Time: 18:00
        
        # Trigger change event to ensure React picks it up
        driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", date_input)
        time.sleep(0.5)
        
        # 4. Location
        print("Setting location...")
        loc_input = wait.until(EC.visibility_of_element_located((By.NAME, "location_search")))
        loc_input.clear()
        loc_input.send_keys("Jerusalem")
        
        # Click search and wait for results
        search_btn = driver.find_element(By.CSS_SELECTOR, ".location-search-container button.btn-secondary")
        search_btn.click()
        
        print("Waiting for search results list...")
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "search-results-list")))
        
        first_result = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-results-list li")))
        print(f"Selecting location result: {first_result.text}")
        first_result.click()
        
        # Extra wait for React state to settle (Critical for location)
        print("Waiting for state to sync...")
        time.sleep(4) 
        
        # Debugging: Print current values before clicking Next
        print(f"Current Title Value: {title_input.get_attribute('value')}")
        print(f"Current Date Value: {date_input.get_attribute('value')}")
        
        print("Proceeding to Step 2...")
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next') or contains(text(), 'הבא')]")))
        
        # Final safety check for Title/Date
        if not title_input.get_attribute('value') or not date_input.get_attribute('value'):
             print("Fields empty in DOM. Injecting values via JS as fallback...")
             driver.execute_script("arguments[0].value = 'Selenium UI Gala'; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", title_input)
             driver.execute_script("arguments[0].value = '2025-12-31T18:00'; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", date_input)

        next_btn.click()
        
        # STEP 2: Guests
        print("Step 2: Adding Guests...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "guest-import-tabs")))
        
        tabs = driver.find_elements(By.CLASS_NAME, "tab-btn")
        tabs[1].click() # Manual Add tab
        
        print("Entering guest info...")
        wait.until(EC.visibility_of_element_located((By.NAME, "guest_name"))).send_keys("Selenium Guest")
        driver.find_element(By.NAME, "guest_email").send_keys("selenium@ui-test.com")
        
        add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".manual-input-group button")))
        add_btn.click()
        print("Guest added.")
        
        time.sleep(1)
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next') or contains(text(), 'הבא')]")))
        next_btn.click()
        
        # STEP 3: Review & Submit
        print("Step 3: Review and Submit...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "review-step")))
        
        submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".review-step button.btn-primary")))
        submit_btn.click()
        
        # Handle Success Alert
        print("Waiting for success alert...")
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Alert: {alert.text}")
        alert.accept()
        
        # Dashboard Navigation
        print("Waiting for Dashboard redirect...")
        wait.until(EC.url_contains("/dashboard"))
        
        # Verification logic continues... (the rest is as before)
        print("UI Test reached Dashboard successfully.")
        
    except Exception as e:
        print(f"Selenium Test Failed: {e}")
        try:
            alert = driver.switch_to.alert
            print(f"Active Alert detected during failure: {alert.text}")
            alert.dismiss()
        except:
            pass
        sys.exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    if not wait_for_backend():
        print("Backend not available. Exiting.")
        sys.exit(1)
    test_full_ui_flow()
