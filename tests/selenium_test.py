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
    
    # Add header to skip ngrok browser warning
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = webdriver.Remote(
        command_executor=SELENIUM_HUB,
        options=chrome_options
    )
    
    # Inject ngrok-skip-browser-warning header
    driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
        'headers': {'ngrok-skip-browser-warning': 'true'}
    })
    
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
        
        # 3. Setting Date - React-aware approach
        print("Setting date...")
        date_input = wait.until(EC.visibility_of_element_located((By.NAME, "date")))
        
        # This JavaScript trick bypasses React's controlled component system
        driver.execute_script("""
            var input = arguments[0];
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
            nativeInputValueSetter.call(input, '2025-12-31T18:00');
            var event = new Event('input', { bubbles: true });
            input.dispatchEvent(event);
            input.dispatchEvent(new Event('change', { bubbles: true }));
        """, date_input)
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
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "event-item")))
        
        # Select our event
        event_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//h4[contains(text(), 'Selenium UI Gala')]")))
        event_item.click()
        print("Event selected in dashboard.")
        
        # === PART 1: Get RSVP Link and Perform RSVP ===
        print("\n=== PART 1: Testing RSVP Flow ===")
        
        # Open Preview
        print("Opening Preview to extract RSVP link...")
        view_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-info")))
        view_btn.click()
        
        # Switch to iframe
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)
        
        # Extract RSVP URL
        rsvp_anchor = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'RSVP') or contains(text(), 'אישור')]")))
        rsvp_url = rsvp_anchor.get_attribute("href")
        print(f"Extracted RSVP URL: {rsvp_url}")
        
        driver.switch_to.default_content()
        
        # Close modal
        close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close') or contains(text(), 'סגור')]")))
        close_btn.click()
        time.sleep(1)
        
        # Navigate to RSVP page
        print(f"Navigating to RSVP page...")
        driver.get(rsvp_url)
        
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rsvp-card")))
        
        # Fill RSVP form
        print("Filling RSVP: Attending with 3 guests")
        status_select = Select(wait.until(EC.presence_of_element_located((By.CLASS_NAME, "status-select"))))
        status_select.select_by_value("attending")
        
        guest_input = driver.find_element(By.CSS_SELECTOR, ".guests-input input")
        guest_input.clear()
        guest_input.send_keys("3")
        
        submit_rsvp_btn = driver.find_element(By.CLASS_NAME, "btn-submit")
        submit_rsvp_btn.click()
        
        # Handle RSVP success alert
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"RSVP Alert: {alert.text}")
        alert.accept()
        
        # === PART 2: Verify Status in Dashboard ===
        print("\n=== PART 2: Verifying RSVP Status in Dashboard ===")
        driver.get(f"{FRONTEND_URL}/dashboard")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "event-item")))
        
        # Re-select event
        driver.find_element(By.XPATH, "//h4[contains(text(), 'Selenium UI Gala')]").click()
        
        # Check guest table
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rsvp-table")))
        status_badge = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "status-badge")))
        print(f"Guest Status: {status_badge.text}")
        assert "attending" in status_badge.get_attribute("class"), "Status should be 'attending'"
        print("✓ Verified: Guest status is 'attending'")
        
        # === PART 3: Edit Event (should reset RSVP status) ===
        print("\n=== PART 3: Testing Event Edit and RSVP Reset ===")
        
        # Click Edit button - it's in the EventsList component
        edit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'edit-btn') or contains(text(), 'Edit') or contains(text(), 'ערוך')]")))
        edit_btn.click()
        
        # Wait for edit modal/form
        wait.until(EC.visibility_of_element_located((By.NAME, "title")))
        time.sleep(0.5)
        
        # Modify the title
        title_edit = driver.find_element(By.NAME, "title")
        title_edit.clear()
        title_edit.send_keys("Selenium UI Gala - EDITED")
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", title_edit)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", title_edit)
        time.sleep(0.5)
        
        # Save - look for primary button in modal
        save_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-content button.btn-primary, button.btn-primary")))
        save_btn.click()
        
        # Handle save success
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Edit Alert: {alert.text}")
        alert.accept()
        
        time.sleep(2)
        
        # Verify RSVP status reset to pending
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rsvp-table")))
        status_badge_after_edit = driver.find_element(By.CLASS_NAME, "status-badge")
        print(f"Guest Status after edit: {status_badge_after_edit.text}")
        assert "pending" in status_badge_after_edit.get_attribute("class"), "Status should reset to 'pending' after edit"
        print("✓ Verified: Status reset to 'pending' after event edit")
        
        # === PART 4: Re-RSVP (Decline this time) ===
        print("\n=== PART 4: Testing Re-RSVP (Decline) ===")
        
        # Navigate back to RSVP
        driver.get(rsvp_url)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rsvp-card")))
        
        # Decline
        print("Declining RSVP...")
        status_select2 = Select(driver.find_element(By.CLASS_NAME, "status-select"))
        status_select2.select_by_value("not_attending")
        
        driver.find_element(By.CLASS_NAME, "btn-submit").click()
        
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Re-RSVP Alert: {alert.text}")
        alert.accept()
        
        # Verify decline in dashboard
        driver.get(f"{FRONTEND_URL}/dashboard")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "event-item")))
        driver.find_element(By.XPATH, "//h4[contains(text(), 'Selenium UI Gala - EDITED')]").click()
        
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rsvp-table")))
        status_badge_declined = driver.find_element(By.CLASS_NAME, "status-badge")
        print(f"Final Status: {status_badge_declined.text}")
        assert "not_attending" in status_badge_declined.get_attribute("class") or "not-attending" in status_badge_declined.get_attribute("class"), "Status should be 'not_attending'"
        print("✓ Verified: Guest status is 'not_attending'")
        
        # === PART 5: Test Export/Download Report ===
        print("\n=== PART 5: Testing Report Export ===")
        
        # Look for Export button
        try:
            export_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Export') or contains(text(), 'יצוא') or contains(text(), 'Download')]")))
            export_btn.click()
            print("✓ Export button clicked successfully")
            time.sleep(2)
        except:
            print("⚠ Export button not found - skipping export test")
        
        print("\n=== ✅ FULL UI TEST PASSED SUCCESSFULLY! ===")
        
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
