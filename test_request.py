# import requests

# url= "http://127.0.0.1:5000/api/review"
# data = {
#     "language": "python",
#     "code": "def greet(name): print(f'Hello, {name}!')"
# }

# response = requests.post(url, json=data)
# print(response.json())

import requests

data = {
    "language": "Python",
    "code": "def add(a, b): return a + b"
}

try:
    response = requests.post("http://127.0.0.1:5000/api/review", json=data)
    print("Status code:", response.status_code)
    print("Response text:", response.text)  # print text first for debugging

    # Only try to parse JSON if it looks like JSON
    if response.headers.get("Content-Type", "").startswith("application/json"):
        print(response.json())
    else:
        print("Non-JSON response received.")

except Exception as e:
    print("Error:", e)
