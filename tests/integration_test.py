import time
import requests
import sys
import os
import json
import random
import string

# Configuration
BASE_URL = "http://localhost:5000"

# Mail.tm API Configuration
MAIL_TM_API = "https://api.mail.tm"
TEST_ACCOUNT = {} # Will store email, password, token, id

def wait_for_service(url, name, retries=30, delay=2):
    print(f"Waiting for {name} at {url}...")
    for i in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"{name} is up!")
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

def get_temp_email():
    """Generate a random temporary email using Mail.tm"""
    global TEST_ACCOUNT
    try:
        # 1. Get Domains
        resp = requests.get(f"{MAIL_TM_API}/domains")
        if resp.status_code != 200:
            print(f"Mail.tm: Failed to get domains: {resp.text}")
            return None
        
        domain = resp.json()['hydra:member'][0]['domain']
        
        # 2. Create Account
        rnd_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
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
        
        # Store account details
        TEST_ACCOUNT = {
            "address": address,
            "password": password,
            "token": token
        }
        
        print(f"Generated temporary email: {address}")
        return address

    except Exception as e:
        print(f"Error generating temp email: {e}")
    return None

def verify_email_received(email_address, retries=30, delay=5):
    """Check Mail.tm for received messages"""
    global TEST_ACCOUNT
    print(f"Waiting for email to arrive at {email_address}...")
    
    if not TEST_ACCOUNT or TEST_ACCOUNT['address'] != email_address:
         print("Error: No matching test account credentials found.")
         return False

    headers = {
        "Authorization": f"Bearer {TEST_ACCOUNT['token']}"
    }
    
    for i in range(retries):
        try:
            # Get messages
            resp = requests.get(f"{MAIL_TM_API}/messages", headers=headers)
            if resp.status_code == 200:
                messages = resp.json()['hydra:member']
                if len(messages) > 0:
                    last_msg = messages[0]
                    print(f"Email received! Subject: {last_msg['subject']}")
                    print(f"From: {last_msg['from']['address']}")
                    return True
            else:
                print(f"Mail.tm check failed: {resp.status_code}")
        except Exception as e:
            print(f"Error checking email: {e}")
            
        time.sleep(delay)
        
    print("Timeout: Email was not received.")
    return False

def test_create_event_and_rsvp():
    print("Testing Event Creation and RSVP...")
    
    # 1. Create Event
    event_data = {
        "title": "Integration Test Event",
        "type": "wedding",
        "date": "2025-12-31T18:00:00",
        "location": "Test Venue",
        # Using a real image from the project (mounted at /app/backgrounds in backend)
        "email_background_url": "http://localhost:3000/src/background/wadding.jpg" 
    }
    
    # Optional: Verify the file actually exists in the backend container (since we mounted it)
    if os.path.exists("/app/backgrounds/wadding.jpg"):
        print("Verified: Background image 'wadding.jpg' exists in /app/backgrounds")
    else:
        print("Warning: Background image 'wadding.jpg' NOT found in /app/backgrounds")

    resp = requests.post(f"{BASE_URL}/api/events", json=event_data)
    if resp.status_code != 201:
        print(f"Failed to create event: {resp.text}")
        return False
    
    event_id = resp.json()['id']
    print(f"Event created with ID: {event_id}")
    
    # 2. Send Invitation
    # Try to generate a real temporary email address
    guest_email = get_temp_email()
    should_verify_email = True
    
    if not guest_email:
        print("Warning: Failed to generate temp email (No Internet?). Using fallback email.")
        guest_email = "test_fallback@example.com"
        should_verify_email = False
        
    guests = [{"name": "Test Guest", "email": guest_email}]
    invite_data = {
        "event_id": event_id,
        "guests": guests
    }
    
    print(f"Sending invitation to {guest_email}...")
    try:
        resp = requests.post(f"{BASE_URL}/api/invitations", json=invite_data)
        if resp.status_code == 201:
            print("Invitation sent successfully (API response).")
            invitations = resp.json()['invitations']
            token = invitations[0]['token']
            
            # Verify email was received by the external service ONLY if we have a real temp email
            if should_verify_email:
                if not verify_email_received(guest_email):
                    print("CRITICAL: Email was not received by the recipient!")
                    return False
            else:
                print("Skipping email verification (using fallback email).")
                
        else:
            print(f"Invitation sending failed: {resp.text}")
            return False
    except Exception as e:
        print(f"Exception during invitation: {e}")
        return False

    # 3. RSVP
    print(f"RSVPing with token: {token}")
    rsvp_data = {
        "status": "attending",
        "guests_count": 1
    }
    
    resp = requests.post(f"{BASE_URL}/api/rsvp/{token}", json=rsvp_data)
    if resp.status_code != 200:
        print(f"RSVP failed: {resp.text}")
        return False
        
    # 4. Verify RSVP
    resp = requests.get(f"{BASE_URL}/api/rsvp/{token}")
    data = resp.json()
    if data['invitation']['status'] == 'attending':
        print("RSVP verification passed: Status is 'attending'.")
        return True
    else:
        print(f"RSVP verification failed: Status is {data['invitation']['status']}")
        return False

def run_tests():
    # Wait for Backend
    if not wait_for_service(f"{BASE_URL}/health", "Backend"):
        sys.exit(1)
    
    if not test_health():
        sys.exit(1)
        
    if not test_create_event_and_rsvp():
        sys.exit(1)
        
    print("All integration tests passed!")

if __name__ == "__main__":
    run_tests()
