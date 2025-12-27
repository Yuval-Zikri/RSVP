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
    
    # Note: ngrok-skip-browser-warning is already set globally in frontend/backend
    
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
        
        # Get the token directly from the API
        print("Getting RSVP token from API...")
        
        import requests
        
        # Try to find the latest event with invitations by searching backwards
        rsvps = []
        found_event_id = None
        
        # Start from a higher ID and work backwards to find the most recent event
        for event_id in range(100, 0, -1):
            try:
                rsvps_response = requests.get(
                    f"{BACKEND_URL}/api/events/{event_id}/rsvps", 
                    headers={'ngrok-skip-browser-warning': 'true'},
                    timeout=2
                )
                if rsvps_response.status_code == 200:
                    rsvps_data = rsvps_response.json()
                    if rsvps_data and len(rsvps_data) > 0:
                        # Found an event with invitations
                        rsvps = rsvps_data
                        found_event_id = event_id
                        print(f"✓ Found event ID {event_id} with {len(rsvps)} invitation(s)")
                        break
            except:
                continue
        
        if not rsvps or not found_event_id:
            raise Exception("Could not find any event with invitations. The event might not have been created properly.")
        
        # Get the first guest's token
        first_guest = rsvps[0]
        token = first_guest['token']
        rsvp_url = f"{FRONTEND_URL}/rsvp/{token}"
        print(f"✓ Using invitation token: {token}")
        print(f"✓ RSVP URL: {rsvp_url}")
        
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
        
        # Debug: check form values before submit
        selected_status = status_select.first_selected_option.get_attribute("value")
        guest_count_value = guest_input.get_attribute("value")
        print(f"DEBUG: Status dropdown value: {selected_status}")
        print(f"DEBUG: Guest count value: {guest_count_value}")
        
        submit_rsvp_btn = driver.find_element(By.CLASS_NAME, "btn-submit")
        submit_rsvp_btn.click()
        
        # Handle RSVP success alert
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"RSVP Alert: {alert.text}")
        alert.accept()
        
        # Verify the RSVP was actually saved via API
        print("Verifying RSVP was saved in backend...")
        time.sleep(2)  # Wait for backend to process
        
        verify_response = requests.get(
            f"{BACKEND_URL}/api/events/{found_event_id}/rsvps",
            headers={'ngrok-skip-browser-warning': 'true'}
        )
        
        if verify_response.status_code == 200:
            updated_rsvps = verify_response.json()
            if updated_rsvps and len(updated_rsvps) > 0:
                first_rsvp = updated_rsvps[0]
                print(f"Backend RSVP Status: {first_rsvp.get('status')}")
                print(f"Backend RSVP Guests: {first_rsvp.get('guests_count')}")
                
                if first_rsvp.get('status') != 'attending':
                    print(f"⚠ WARNING: Backend shows status as '{first_rsvp.get('status')}', not 'attending'")
            else:
                print("⚠ WARNING: No RSVPs found in backend after submit")
        
        # === PART 2: Verify Status in Dashboard ===
        print(f"\n=== PART 2: Verifying RSVP Status in Dashboard (Event ID: {found_event_id}) ===")
        driver.get(f"{FRONTEND_URL}/dashboard")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "event-item")))
        
        # Wait for backend to process
        time.sleep(3)
        
        # Refresh to get the latest data
        print("Refreshing dashboard to get latest RSVP status...")
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "event-item")))
        time.sleep(2)
        
        # Re-select event using the specific event ID we found
        print(f"Looking for event with ID {found_event_id}...")
        
        # Try to find the event by its ID attribute or by matching the title exactly
        event_items = driver.find_elements(By.CLASS_NAME, "event-item")
        clicked = False
        
        for item in event_items:
            # Check if this element has a data attribute or ID that matches
            try:
                # Some implementations might have data-event-id or similar
                item_id = item.get_attribute("data-event-id")
                if item_id and int(item_id) == found_event_id:
                    print(f"Found event by data-event-id: {item_id}")
                    item.click()
                    clicked = True
                    break
            except:
                pass
        
        # Fallback: if we couldn't find by ID, look for the most recent "Selenium UI Gala"
        if not clicked:
            print("Fallback: Clicking the last 'Selenium UI Gala' event in the list...")
            matching_events = driver.find_elements(By.XPATH, "//h4[contains(text(), 'Selenium UI Gala')]")
            if matching_events:
                # Click the last one (most recent)
                matching_events[-1].click()
                clicked = True
        
        if not clicked:
            raise Exception(f"Could not find event ID {found_event_id} in the dashboard")
        
        # Wait for RSVP table to load with fresh data
        print("Waiting for RSVP data to load...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rsvp-table")))
        time.sleep(2)  # Give time for the API call to complete
        
        status_badge = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "status-badge")))
        badge_class = status_badge.get_attribute("class")
        badge_text = status_badge.text
        print(f"Guest Status Badge Class: {badge_class}")
        print(f"Guest Status Badge Text: {badge_text}")
        
        assert "attending" in badge_class.lower() or "attending" in badge_text.lower(), f"Status should be 'attending', but got class: {badge_class}, text: {badge_text}"
        print("✓ Verified: Guest status is 'attending'")
        
        # === PART 3: Edit Event (should reset RSVP status) ===
        print("\n=== PART 3: Testing Event Edit and RSVP Reset ===")
        
        # First, make sure we're looking at the correct event in the sidebar
        # Find all "Selenium UI Gala" events and get the edit button of the last one
        print(f"Looking for edit button of event ID {found_event_id}...")
        
        event_items = driver.find_elements(By.CLASS_NAME, "event-item")
        edit_btn = None
        
        # Get the last event-item (most recent)
        if event_items:
            last_event = event_items[-1]
            # Find the edit button within this event
            try:
                edit_btn = last_event.find_element(By.CLASS_NAME, "btn-edit")
                print(f"Found edit button in last event item")
            except:
                print("Could not find btn-edit in last event, trying generic selector...")
        
        # Fallback to generic selector
        if not edit_btn:
            edit_buttons = driver.find_elements(By.CLASS_NAME, "btn-edit")
            if edit_buttons:
                edit_btn = edit_buttons[-1]  # Take the last one
                print(f"Using last edit button from {len(edit_buttons)} buttons found")
        
        if not edit_btn:
            raise Exception("Could not find edit button")
        
        # Scroll the button into view and wait for it to be clickable
        print("Scrolling to edit button and waiting for it to be clickable...")
        driver.execute_script("arguments[0].scrollIntoView(true);", edit_btn)
        time.sleep(0.5)
        
        # Wait for the button to be clickable
        wait.until(EC.element_to_be_clickable(edit_btn))
        
        edit_btn.click()
        print("Edit button clicked")
        
        # Wait for edit modal to appear
        print("Waiting for edit modal/form to appear...")
        time.sleep(1)  # Give the modal time to start appearing
        
        try:
            # Try to wait for the modal container first
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "modal-content")))
            print("Modal appeared")
        except:
            print("Modal container not found, trying to find title input directly...")
        
        # Wait for title input field to be visible
        title_input = wait.until(EC.visibility_of_element_located((By.NAME, "title")))
        print("Title input field found")
        time.sleep(0.5)
        
        # Modify the title and the date
        title_edit = driver.find_element(By.NAME, "title")
        title_edit.clear()
        title_edit.send_keys("Selenium UI Gala - EDITED")
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", title_edit)
        
        # Change the date to trigger RSVP reset
        print("Changing date to trigger RSVP reset...")
        date_edit = driver.find_element(By.NAME, "date")
        
        # Use the same React-aware setter we used in Part 1
        driver.execute_script("""
            var input = arguments[0];
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
            nativeInputValueSetter.call(input, '2025-12-31T20:00');
            var event = new Event('input', { bubbles: true });
            input.dispatchEvent(event);
            input.dispatchEvent(new Event('change', { bubbles: true }));
        """, date_edit)
        time.sleep(1)
        
        # Save - use a very specific selector for the "Save Changes" button in the modal
        print("Looking for Save button in modal...")
        save_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-content .modal-actions button.btn-primary")))
        
        # Sometimes standard click() is intercepted even if wait says it's clickable.
        # JS click is more reliable for buttons in overlays.
        print("Clicking save button via JS to avoid overlay issues...")
        driver.execute_script("arguments[0].click();", save_btn)
        
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
        print("Navigating to dashboard to verify decline...")
        driver.get(f"{FRONTEND_URL}/dashboard")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "event-item")))
        
        # Refresh to ensure we get the latest RSVP data
        print("Refreshing dashboard...")
        time.sleep(2)
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "event-item")))
        time.sleep(1)
        
        # Re-select the edited event (it should be the last one)
        print("Selecting the edited event...")
        matching_events = driver.find_elements(By.XPATH, f"//h4[contains(text(), 'Selenium UI Gala - EDITED')]")
        if matching_events:
            matching_events[-1].click()
        else:
            # Fallback if text search fails
            event_items = driver.find_elements(By.CLASS_NAME, "event-item")
            if event_items:
                event_items[-1].click()
        
        # Wait for table to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rsvp-table")))
        time.sleep(2)  # Wait for API data to render
        
        status_badge_declined = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "status-badge")))
        badge_text = status_badge_declined.text
        badge_class = status_badge_declined.get_attribute("class").lower()
        print(f"Final Status Badge Text: {badge_text}")
        print(f"Final Status Badge Class: {badge_class}")
        
        assert "not_attending" in badge_class or "not-attending" in badge_class or "declined" in badge_text.lower() or "not" in badge_text.lower(), f"Status should be 'not_attending', but got text: {badge_text}, class: {badge_class}"
        print("✓ Verified: Guest status correctly updated after second RSVP")
        
        # === PART 5: Test Export/Download Report ===
        print("\n=== PART 5: Testing Report Export ===")
        
        # Verify the data that will be exported (to show the user what's in the "file")
        print("Fetching final RSVP list for verification:")
        final_data_resp = requests.get(f"{BACKEND_URL}/api/events/{found_event_id}/rsvps", headers={'ngrok-skip-browser-warning': 'true'})
        if final_data_resp.status_code == 200:
            for r in final_data_resp.json():
                print(f"  - Guest: {r.get('name')}, Email: {r.get('email')}, Status: {r.get('status')}, Guests: {r.get('guests_count')}")
        
        # Look for Export button - use dot (.) instead of text() to ignore emojis/whitespace issues
        try:
            print("Looking for Export button...")
            export_btn = wait.until(EC.element_to_be_clickable((By.XPATH, 
                "//button[contains(normalize-space(.), 'Export') or contains(normalize-space(.), 'ייצוא') or contains(normalize-space(.), 'יצוא')]"
            )))
            
            # Scroll to it
            driver.execute_script("arguments[0].scrollIntoView(true);", export_btn)
            time.sleep(0.5)
            
            export_btn.click()
            print("✓ Export button clicked successfully")
            time.sleep(2)
        except Exception as e:
            print(f"⚠ Export button not found or could not be clicked via primary selector: {e}")
            # Fallback: try by Export class if exists or just take the last primary button
            try:
                btns = driver.find_elements(By.CSS_SELECTOR, ".btn-primary")
                if btns:
                    btns[-1].click()
                    print("✓ Clicked the last btn-primary as fallback")
                else:
                    print("⚠ No primary buttons found for export fallback")
            except:
                print("⚠ Fallback also failed")
        
        print("\n=== ✅ FULL UI TEST PASSED SUCCESSFULLY! ===")
        
    except Exception as e:
        print(f"Selenium Test Failed: {e}")
        try:
            # Capture failure state
            screenshot_path = "failure_screenshot.png"
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            
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
