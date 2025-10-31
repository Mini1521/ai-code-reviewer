import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"                      #base URL for the Flask backend

set_1 = [                                               #to test the review system ,sample code in multiple languages 
    {"language": "Python","code": "def add(a, b):\n    return a + b" },
    {"language": "Java","code": "public class HelloWorld { public static void main(String[] args) { System.out.println(\"Hello, Java!\"); } }"},
    {"language": "C++","code": "#include <iostream>\nint main() { std::cout << \"Hello, C++!\" << std::endl; return 0; }"},
    {"language": "C#","code": "using System;\nclass Program { static void Main() { Console.WriteLine(\"Hello, C#\"); } }"},
    {"language": "JavaScript","code": "function greet(name) { console.log('Hello, ' + name + '!'); }\ngreet('World');"}
]

 #sample test used to check API error handling and input validation
set_2 = [
    {"language": "Python",
     "code": ""                                         #empty code 
    },
    {"language": "Python",
     "code": "def broken_func(:\n    pass"              #syntax error (invalid Python)
    },
    {"language": "JavaScript",
     "code": "console.log('Unclosed string);"   
    },        
    {"language": "C++",
     "code": "int main() { return 0; }"                 
    },
    {"language": "C#",
     "code": "using System;\nclass Program { static void Main() { Console.Writeline('Missing Semicolon') } }"  
    },
    {"language": "Python",
     "code": "print('x' * 10000)"                       #very long output case (stress test)
    }
]

def post_review(sample):                #function to create new review
    print(f" Sending review request for {sample['language']} code...")
    response = requests.post(f"{BASE_URL}/api/review", json=sample)
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    time.sleep(2)                       # slight delay to avoid rate limits


def get_all_reviews():                  #function to get all reviews and display them
    print("\n Fetching all reviews...")
    response = requests.get(f"{BASE_URL}/api/reviews")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_delete_review(review_id):      #function to delete a single review by ID
    print(f"\n Deleting review {review_id} ...")
    r = requests.delete(f"{BASE_URL}/api/review/{review_id}")
    print("Status:", r.status_code)
    try:
        print(json.dumps(r.json(), indent=2))
    except:
        print(r.text)

if __name__ == "__main__":              # main function , runs when file is executed
    print(" Starting multi-language review test...\n")
    for s in set_1:                   #post each sample review and get all reviews after each post
        post_review(s)
    get_all_reviews()                   #new reviews are displayed

    print("\n Starting error handling test...\n")
    for r in set_2:
        post_review(r)
    get_all_reviews()                   #all reviews including error cases are displayed

if __name__ == "__main__":              #main function to delete a review by ID
    post_review({"language":"Python","code":"def add(a,b): return a+b"})
    get_all_reviews()
    test_delete_review(5)               #change id to the one you want to delete or parse previous response to get id
    get_all_reviews()

#--- To delete all reviews, uncomment below ---#
# requests.delete(f"{BASE_URL}/api/reviews")
# print("\n Deleting all reviews ...")