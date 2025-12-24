import time
import requests
import sys
import os
import json

# Configuration
BASE_URL = "http://localhost:5000"

# 1secmail API Configuration
ONESECMAIL_API = "https://www.1secmail.com/api/v1/"
# Fake User-Agent to avoid 403 Forbidden
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

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
    """Generate a random temporary email using 1secmail"""
    try:
        resp = requests.get(f"{ONESECMAIL_API}?action=genRandomMailbox&count=1", headers=HEADERS)
        if resp.status_code == 200:
            email = resp.json()[0]
            print(f"Generated temporary email: {email}")
            return email
        else:
            print(f"Error generating temp email: Status {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Error generating temp email: {e}")
    return None

def verify_email_received(email_address, retries=30, delay=5):
    """Check 1secmail for received messages"""
    print(f"Waiting for email to arrive at {email_address}...")
    try:
        login, domain = email_address.split('@')
    except ValueError:
        print(f"Invalid email address format: {email_address}")
        return False
    
    for i in range(retries):
        try:
            # Check mailbox
            resp = requests.get(f"{ONESECMAIL_API}?action=getMessages&login={login}&domain={domain}", headers=HEADERS)
            if resp.status_code == 200:
                messages = resp.json()
                if len(messages) > 0:
                    last_msg = messages[0]
                    print(f"Email received! Subject: {last_msg['subject']}")
                    print(f"From: {last_msg['from']}")
                    return True
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
