import requests
import time
import random
import json
from datetime import datetime

# Config
API_URL = "http://localhost:8000/sensors/"  # Change for prod
ACCESS_TOKEN = "your-jwt-token-here"  # Get from login; for demo, hardcode or automate
LAND_ID = 1  # Assume land ID 1 exists; change as needed

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def send_fake_sensor_data():
    data = {
        "land_id": LAND_ID,
        "moisture": random.uniform(10, 50),  # %
        "ph": random.uniform(5.5, 7.5),
        "temperature": random.uniform(20, 35)  # Celsius
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        if response.status_code == 200:
            print(f"[{datetime.now()}] Sent sensor data: {data} | NDVI analysis triggered")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Simulator error: {e}")

if __name__ == "__main__":
    print("Starting IoT Simulator... Press Ctrl+C to stop.")
    while True:
        send_fake_sensor_data()
        time.sleep(10)  # Send every 10 seconds