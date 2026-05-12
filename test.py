# test.py

import requests
import time

URL = "http://127.0.0.1:8000/generate"

for i in range(5):

    print(f"\nRequest {i+1}")

    start = time.time()

    response = requests.get(URL)

    end = time.time()

    print("Response:", response.json())

    print("Time Taken:", round(end - start, 2), "seconds")

    print("-" * 40)
