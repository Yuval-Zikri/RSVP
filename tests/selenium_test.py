import time
import requests
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Configuration
# Note: Inside Jenkins/Docker, we use the service names defined in docker-compose.yaml
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
        
        # Select Wedding - updated selector to match div.event-type-name-primary
        wedding_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'event-type-name-primary') and (contains(text(), 'Wedding') or contains(text(), 'חתונה'))]")))
        wedding_card.click()
        
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next') or contains(text(), 'הבא')]")))
        next_btn.click()
        
        # STEP 1: Event Details
        print("Step 1: Filling Event Details...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "form-step")))
        
        # 1. Enter Title using direct NAME selector and JS as backup
        print("Entering title...")
        title_input = wait.until(EC.presence_of_element_located((By.NAME, "title")))
        title_input.clear()
        title_input.send_keys("Selenium UI Gala")
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", title_input)
        
        # 2. Enter Subtitle
        print("Entering subtitle...")
        subtitle_input = wait.until(EC.presence_of_element_located((By.NAME, "subtitle")))
        subtitle_input.clear()
        subtitle_input.send_keys("Automated Test Runner")
        
        # 3. Setting Date
        print("Setting date...")
        date_input = driver.find_element(By.CSS_SELECTOR, "input[type='datetime-local']")
        driver.execute_script("""
            var el = arguments[0];
            el.value = '2025-12-31T18:00';
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        """, date_input)
        
        # 4. Location - This part is critical. We search and must ensure selection happens.
        print("Setting location...")
        loc_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".location-search-container input")))
        loc_input.clear()
        loc_input.send_keys("Jerusalem")
        
        # Click search and wait for results
        search_btn = driver.find_element(By.CSS_SELECTOR, ".location-search-container button.btn-secondary")
        search_btn.click()
        
        print("Waiting for search results list...")
        # Wait for the UL to appear
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-results-list")))
        
        # Find and click the first LI
        first_result = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-results-list li")))
        print(f"Selecting location result: {first_result.text}")
        first_result.click()
        
        # Verification: Wait a bit and check if a "Next" button click works
        time.sleep(2) 
        
        print("Proceeding to Step 2...")
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next') or contains(text(), 'הבא')]")))
        next_btn.click()
        
        # (Moving to Step 2)
        # STEP 2: Guests
        print("Step 2: Adding Guests...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "guest-import-tabs")))
        
        # Click Manual Add tab
        tabs = driver.find_elements(By.CLASS_NAME, "tab-btn")
        tabs[1].click()
        
        manual_inputs = driver.find_elements(By.CSS_SELECTOR, ".manual-input-group input")
        manual_inputs[0].send_keys("Selenium Guest")
        manual_inputs[1].send_keys("selenium@ui-test.com")
        
        add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".manual-input-group button")))
        add_btn.click()
        print("Guest added.")
        
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next') or contains(text(), 'הבא')]")))
        next_btn.click()
        
        # STEP 3: Review & Submit
        print("Step 3: Review and Submit...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "review-step")))
        
        # In step 3, there's a primary button to confirm
        submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".review-step button.btn-primary")))
        submit_btn.click()
        
        # Handle Success Alert
        print("Waiting for success alert...")
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Alert: {alert.text}")
        alert.accept()
        
        # 2. Redirect to Dashboard
        print("Waiting for Dashboard redirect...")
        wait.until(EC.url_contains("/dashboard"))
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "event-item")))
        
        # Find our event in the list
        event_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//h4[contains(text(), 'Selenium UI Gala')]")))
        event_item.click()
        print("Event selected in dashboard.")
        
        # 3. Get RSVP Link from Preview
        print("Opening Preview to get RSVP link...")
        view_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-info")))
        view_btn.click()
        
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        
        # Switch to iframe to find the link
        driver.switch_to.frame(iframe)
        rsvp_anchor = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'RSVP') or contains(text(), 'אישור')]")))
        rsvp_url = rsvp_anchor.get_attribute("href")
        print(f"Extracted RSVP URL: {rsvp_url}")
        
        driver.switch_to.default_content()
        # Close modal - It's usually a button with "Close" or an X
        close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close') or contains(text(), 'סגור')]")))
        close_btn.click()
        
        # 4. Perform RSVP
        print(f"Navigating to RSVP page: {rsvp_url}")
        driver.get(rsvp_url)
        
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rsvp-card")))
        
        # Change status
        status_select = Select(driver.find_element(By.CLASS_NAME, "status-select"))
        status_select.select_by_value("attending")
        
        # Set guests
        guest_input = driver.find_element(By.CSS_SELECTOR, ".guests-input input")
        guest_input.clear()
        guest_input.send_keys("5")
        
        driver.find_element(By.CLASS_NAME, "btn-submit").click()
        
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"RSVP Alert: {alert.text}")
        alert.accept()
        
        # 5. Final Verification in Dashboard
        print("Final check: verifying status in Dashboard...")
        driver.get(f"{FRONTEND_URL}/dashboard")
        
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "event-card")))
        # Re-select the event
        driver.find_element(By.XPATH, "//h4[contains(text(), 'Selenium UI Gala')]").click()
        
        # Check the table for our guest
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rsvp-table")))
        
        status_badge = driver.find_element(By.CLASS_NAME, "status-badge")
        print(f"Final guest status in UI: {status_badge.text}")
        assert "attending" in status_badge.get_attribute("class")
        
        print("\n=== FULL UI TEST PASSED SUCCESSFULLY! ===")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    if not wait_for_backend():
        print("Backend not available. Exiting.")
        sys.exit(1)
        
    try:
        test_full_ui_flow()
    except Exception as e:
        print(f"Selenium Test Failed: {e}")
        # Try to take screenshot for debugging if failed
        sys.exit(1)
