import urllib.request
import time

def get_metric():
    try:
        data = urllib.request.urlopen('http://localhost:5000/metrics').read().decode()
        for line in data.split('\n'):
            if line.startswith('location_searches_total'):
                return float(line.split()[-1])
    except Exception as e:
        print(f"Error getting metric: {e}")
    return 0.0

def hit_endpoint():
    try:
        urllib.request.urlopen('http://localhost:5000/api/search-location')
        return True
    except Exception as e:
        print(f"Error hitting endpoint: {e}")
        return False

initial = get_metric()
print(f"Initial metric value: {initial}")

hits = 5
success_hits = 0
for i in range(hits):
    if hit_endpoint():
        success_hits += 1

time.sleep(1) # Give it a moment just in case
final = get_metric()
print(f"Final metric value after {success_hits} hits: {final}")

if final == initial + success_hits:
    print("SUCCESS: Metric incremented correctly!")
else:
    print(f"FAILURE: Expected {initial + success_hits}, got {final}")
