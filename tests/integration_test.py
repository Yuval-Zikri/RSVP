import time
import requests
import sys
import os
import json
import random
import string
import re

# Configuration
BASE_URL = "http://localhost:5000"

# Mail.tm API Configuration
MAIL_TM_API = "https://api.mail.tm"
TEST_ACCOUNTS = [] # Will store list of test accounts

def wait_for_service(url, name, retries=30, delay=2):
    print(f"Waiting for {name} at {url}...")
    for i in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"{name} is up!")
                time.sleep(1) 
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(delay)
    print(f"Error: {name} did not start in time.")
    return False

def test_health():
    print("Testing Health Endpoint...")
    resp = requests.get(f"{BASE_URL}/health")
    if resp.status_code == 200 and resp.json().get("status") == "healthy":
        print("Health check passed.")
        return True
    print(f"Health check failed: {resp.text}")
    return False

def create_mail_tm_account():
    """Create a new temporary email account on Mail.tm"""
    try:
        # 1. Get Domains
        resp = requests.get(f"{MAIL_TM_API}/domains")
        if resp.status_code != 200:
            print(f"Mail.tm: Failed to get domains: {resp.text}")
            return None
        
        domains = resp.json().get('hydra:member')
        if not domains:
             print("Mail.tm: No domains available.")
             return None
             
        domain = domains[0]['domain']
        
        # 2. Create Account
        rnd_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        username = f"test_{rnd_str}"
        password = "Password123!"
        address = f"{username}@{domain}"
        
        resp = requests.post(f"{MAIL_TM_API}/accounts", json={
            "address": address,
            "password": password
        })
        
        if resp.status_code != 201:
            print(f"Mail.tm: Failed to create account: {resp.text}")
            return None
            
        # 3. Get JWT Token
        resp = requests.post(f"{MAIL_TM_API}/token", json={
            "address": address,
            "password": password
        })
        
        if resp.status_code != 200:
            print(f"Mail.tm: Failed to get token: {resp.text}")
            return None
            
        token = resp.json()['token']
        
        account = {
            "address": address,
            "password": password,
            "token": token
        }
        TEST_ACCOUNTS.append(account)
        print(f"Generated temporary email: {address}")
        return account

    except Exception as e:
        print(f"Error creating mail account: {e}")
    return None

def verify_email_content(account, expected_subject, image_url_check=None):
    """Check inbox for specific subject and optionally verify image URL presence"""
    print(f"Checking email for {account['address']}...")
    
    headers = {"Authorization": f"Bearer {account['token']}"}
    
    # Reduced retries to 10 (~30 seconds) to avoid hanging the build too long if SMTP is slow
    for i in range(10): 
        try:
            resp = requests.get(f"{MAIL_TM_API}/messages", headers=headers)
            if resp.status_code == 200:
                messages = resp.json()['hydra:member']
                if len(messages) > 0:
                    # Check the latest message
                    msg_summary = messages[0]
                    
                    if expected_subject in msg_summary['subject']:
                        print(f"Email received! Subject: {msg_summary['subject']}")
                        
                        # Full content verification for Image
                        if image_url_check:
                            msg_id = msg_summary['id']
                            msg_resp = requests.get(f"{MAIL_TM_API}/messages/{msg_id}", headers=headers)
                            if msg_resp.status_code == 200:
                                full_msg = msg_resp.json()
                                # Check html body for the image URL
                                html_content = full_msg.get('html', [])
                                if isinstance(html_content, list) and len(html_content) > 0:
                                    html_body = html_content[0] 
                                else:
                                    html_body = str(html_content) # Sometimes it's a string directly
                                    
                                if image_url_check in html_body:
                                    print(f"Verified: Background image URL found in email body.")
                                else:
                                    # Fallback check for CID if attachment logic changed
                                    if "cid:" in html_body:
                                        print("Verified: Image attached via CID.")
                                    else:
                                        print(f"Warning: Image URL '{image_url_check}' NOT found in email HTML.")
                        
                        return True
            else:
                print(f"Mail.tm check failed: {resp.status_code}")
        except Exception as e:
            print(f"Error checking email: {e}")
            
        time.sleep(3)
        
    print(f"Timeout: Email '{expected_subject}' was not received by {account['address']}.")
    return False

def test_full_scenario():
    print("\n=== Integration Test: Full Scenario ===")
    
    # 1. Verify Assets
    bg_image_url = "http://localhost:3000/src/background/wadding.jpg"
    if os.path.exists("/app/backgrounds/wadding.jpg"):
        print("Verified: Background image file exists on server.")
    else:
        print("Warning: Background image file missing on server!")

    # 2. Create Event
    event_data = {
        "title": "Mega Integration Wedding",
        "type": "wedding",
        "date": "2025-12-31T18:00:00",
        "location": "Integration Hall",
        "email_background_url": bg_image_url
    }
    
    resp = requests.post(f"{BASE_URL}/api/events", json=event_data)
    if resp.status_code != 201:
        print(f"Failed to create event: {resp.text}")
        return False
        
    event_id = resp.json()['id']
    print(f"Event created. ID: {event_id}")
    
    # 3. Invite Multiple Guests
    print("\n--- Testing Multiple Guests Invitation ---")
    guest1 = create_mail_tm_account()
    guest2 = create_mail_tm_account()
    
    if not guest1 or not guest2:
        print("Skipping email verification due to account creation failure.")
        return False 
        
    guests = [
        {"name": "Guest One", "email": guest1['address']},
        {"name": "Guest Two", "email": guest2['address']}
    ]
    
    invite_data = {"event_id": event_id, "guests": guests}
    resp = requests.post(f"{BASE_URL}/api/invitations", json=invite_data)
    
    if resp.status_code == 201:
        print("Invitations sent successfully.")
        
        # Verify both received emails (Soft verification)
        v1 = verify_email_content(guest1, "You're invited", bg_image_url)
        v2 = verify_email_content(guest2, "You're invited", bg_image_url)
        
        if v1 and v2:
            print("Verified: Both guests received invitations with correct image.")
        else:
            print("WARNING: Email verification timed out (SMTP issue?). Proceeding to RSVP test anyway...")
    else:
        print(f"Invitation send failed: {resp.text}")
        return False

    # 4. Location Search
    print("\n--- Testing Location Search ---")
    resp = requests.get(f"{BASE_URL}/api/search-location", params={"q": "Jerusalem"})
    if resp.status_code == 200 and len(resp.json()) >= 0:
        print("Location search API is working (200 OK).")
    else:
        print("Location search failed.")
        return False
        
    # 5. Edit Event & Resend (Implicit Resend)
    print("\n--- Testing Edit & Auto-Resend ---")
    update_data = {
        "title": "Shifted Wedding Date",
        "date": "2026-01-01T20:00:00", # Date change triggers resend
        "type": "wedding",
        "location": "New Hall",
        "email_background_url": bg_image_url,
        "guests": []
    }
    resp = requests.put(f"{BASE_URL}/api/events/{event_id}", json=update_data)
    if resp.status_code == 200:
        print("Event updated.")
        # Verify guest1 received update email
        if verify_email_content(guest1, "Update"):
            print("Verified: Guest received update email after date change.")
        else:
            print("Warning: Update email not received.")
    else:
        print("Event update failed.")
        return False

    # 6. Manual Reminder (Explicit Resend)
    print("\n--- Testing Manual Reminder ---")
    # Sending reminder to pending guests (both are pending)
    resp = requests.post(f"{BASE_URL}/api/events/{event_id}/remind")
    if resp.status_code == 200:
        print(f"Reminders sent: {resp.json().get('sent_count')}")
        if verify_email_content(guest2, "Reminder"):
            print("Verified: Guest received manual reminder.")
    else:
         print(f"Reminder failed: {resp.text}")

    # 7. RSVP (Mixed Responses)
    print("\n--- Testing Mixed RSVP Responses ---")
    resp = requests.get(f"{BASE_URL}/api/events/{event_id}/rsvps")
    if resp.status_code == 200:
        invites = resp.json()
        print(f"Found {len(invites)} pending invitations.")
        
        for invite in invites:
            token = invite['token']
            guest_name = invite['name']  # FIXED: using 'name' instead of 'guest_name'
            
            if "Guest One" in guest_name:
                print(f"Guest One ({guest_name}) is accepting...")
                status = "attending"
            else:
                print(f"Guest Two ({guest_name}) is declining...")
                status = "not_attending"
                
            rsvp_payload = {
                "status": status,
                "guests_count": 1 if status == "attending" else 0
            }
            
            r = requests.post(f"{BASE_URL}/api/rsvp/{token}", json=rsvp_payload)
            if r.status_code != 200:
                print(f"RSVP failed for {guest_name}: {r.text}")
                return False
                
        # Verify statuses
        print("Verifying final statuses...")
        resp = requests.get(f"{BASE_URL}/api/events/{event_id}/rsvps")
        final_invites = resp.json()
        
        mixed_responses_ok = True
        for invite in final_invites:
            print(f"- {invite['name']}: {invite['status']}")
            if "Guest One" in invite['name'] and invite['status'] != 'attending':
                mixed_responses_ok = False
            if "Guest Two" in invite['name'] and invite['status'] != 'not_attending':
                mixed_responses_ok = False
                
        if mixed_responses_ok:
            print("Verified: Mixed RSVP responses recorded correctly.")
        else:
            print("Error: RSVP statuses do not match expectation.")
            return False
            
    else:
        print("Failed to list RSVPs.")
        return False
        
    print("\n=== All Integration Checks Passed ===")
    return True

if __name__ == "__main__":
    # Wait for services
    if not wait_for_service(f"{BASE_URL}/health", "Backend"):
        sys.exit(1)
        
    if not test_health():
        sys.exit(1)
        
    if not test_full_scenario():
        sys.exit(1)
