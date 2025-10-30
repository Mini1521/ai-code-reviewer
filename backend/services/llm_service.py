import os
from openai import OpenAI
from dotenv import load_dotenv
import re

load_dotenv()                               #load environment variables from .env
api_key = os.getenv("OPENAI_API_KEY")       #fetch API key securely
client = OpenAI(api_key=api_key)            #create OpenAI client

def analyze_code(language, code):           #function to analyze code snippets
    if not api_key:                         #error message returned, if API key missing
        return {
            "review": "Error: No OpenAI API key found. Please set it in the .env file.",
            "score": 0
        }

    try:                                    #chat completion request sent to OpenAI (using GPT-4o-mini model  )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert code reviewer. "
                        "Analyze the given code and provide constructive feedback "
                        "about clarity, efficiency, and readability. "
                        "Rate the code from 1 to 10."
                    ),
                },
                {
                    "role": "user", #user's message with code snippet and language
                    "content": f"Language: {language}\n\nCode:\n{code}"
                },
            ],
            temperature=0.5, #more consistent feedback with moderate creativity
        )

        review_text = response.choices[0].message.content.strip() #text extracted from the API response

        review_text = (     #text formatting for frontend display
            review_text.replace("###", "\n\n###")       # add spacing before headings
                        .replace("####", "\n- **")      # bullet point style for clarity
                        .replace("**:", "**:**")        # fix bold colon spacing
                        .replace("### ", "\n\n### ")    # better readability in frontend
        )
 
        match = re.search(r'(\d+)\s*out\s*of\s*10', review_text) #score extracted from the review
        score = int(match.group(1)) 

        return { #everything returned to frontend
            "review": review_text,
            "score": score
        }

    except Exception as e: #handle any unexpected errors during API call
        return {
            "review": f" Error analyzing code: {str(e)}",
            "score": 0
        }