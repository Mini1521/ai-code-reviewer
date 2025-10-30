import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

samples = [
    {
        "language": "Python",
        "code": "def add(a, b):\n    return a + b"
    },
    {
        "language": "Java",
        "code": "public class HelloWorld { public static void main(String[] args) { System.out.println(\"Hello, Java!\"); } }"
    },
    {
        "language": "C++",
        "code": "#include <iostream>\nint main() { std::cout << \"Hello, C++!\" << std::endl; return 0; }"
    },
    {
        "language": "C#",
        "code": "using System;\nclass Program { static void Main() { Console.WriteLine(\"Hello, C#\"); } }"
    }
]


def post_review(sample):
    print(f"🔹 Sending review request for {sample['language']} code...")
    response = requests.post(f"{BASE_URL}/api/review", json=sample)
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    time.sleep(2)  # slight delay to avoid rate limits


def get_all_reviews():
    print("\n🔹 Fetching all reviews...")
    response = requests.get(f"{BASE_URL}/api/reviews")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    print("🚀 Starting multi-language review test...\n")
    for s in samples:
        post_review(s)
    get_all_reviews()

def test_delete_review(review_id):
    print(f"\n🔹 Deleting review {review_id} ...")
    r = requests.delete(f"{BASE_URL}/api/review/{review_id}")
    print("Status:", r.status_code)
    try:
        print(json.dumps(r.json(), indent=2))
    except:
        print(r.text)


if __name__ == "__main__":
    # example: post one review, get all, then delete the last one
    post_review({"language":"Python","code":"def add(a,b): return a+b"})
    get_all_reviews()
    # change id to the one you want to delete or parse previous response to get id
    test_delete_review(5)
    get_all_reviews()

