import threading
import requests
import time
# def make_request():
#     try:
#         response = requests.get("http://127.0.0.1:5001/drivers")
#         print(f"Status Code: {response.status_code}, Response: {response.text}")
#     except Exception as e:
#         print(f"Request failed: {e}")

# threads = []
# for _ in range(100):  # Simulate 100 users
#     thread = threading.Thread(target=make_request)
#     threads.append(thread) 
#     thread.start()

# for thread in threads:
#     thread.join()








# Results storage
success_count = 0
failure_count = 0
response_times = []

# Lock for thread-safe updates
lock = threading.Lock()

def make_request():
    global success_count, failure_count, response_times
    try:
        start_time = time.time()
        response = requests.get("http://127.0.0.1:5001/drivers")
        elapsed_time = time.time() - start_time
        
        with lock:
            response_times.append(elapsed_time)
            if response.status_code == 200:
                success_count += 1
            else:
                failure_count += 1
    except Exception as e:
        with lock:
            failure_count += 1
        print(f"Request failed: {e}")

threads = []
for _ in range(100):  # Simulate 100 users
    thread = threading.Thread(target=make_request)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

# Summary
print(f"Total Requests: {len(response_times) + failure_count}")
print(f"Successful Requests: {success_count}")
print(f"Failed Requests: {failure_count}")
if response_times:
    print(f"Average Response Time: {sum(response_times) / len(response_times):.2f} seconds")
    print(f"Max Response Time: {max(response_times):.2f} seconds")
    print(f"Min Response Time: {min(response_times):.2f} seconds")
