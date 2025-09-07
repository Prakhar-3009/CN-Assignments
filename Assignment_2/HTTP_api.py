import requests
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def http_get(url: str):
    logging.info(f"GET {url}")
    try:
        response = requests.get(url, timeout=10)
        print("\n[GET]")
        print(f"Status: {response.status_code}")
        print(f"Body snippet:\n{response.text[:200]}...\n") 
    except requests.exceptions.RequestException as e:
        logging.error(f"GET failed: {e}")

def http_post(url: str, data: dict):
    logging.info(f"POST {url}")
    try:
        response = requests.post(url, json=data, timeout=10)
        print("\n[POST]")
        print(f"Status: {response.status_code}")
        print(f"Body snippet:\n{response.text[:200]}...\n")  
    except requests.exceptions.RequestException as e:
        logging.error(f"POST failed: {e}")

if __name__ == "__main__":
    test_get_url = "https://httpbin.org/get"
    test_post_url = "https://httpbin.org/post"
    post_data = {"assignment": "Computer Networks", "Lab2": "HTTP task"}
    
    http_get(test_get_url)
    http_post(test_post_url, post_data)
