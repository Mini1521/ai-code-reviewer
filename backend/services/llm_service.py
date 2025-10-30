import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch API key securely
api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
client = OpenAI(api_key=api_key)

def analyze_code(language, code):
    """
    This function sends the code snippet and its language
    to OpenAI's model for review and improvement suggestions.
    It returns the model's feedback and an approximate score.
    """

    # If API key is missing, show a helpful message
    if not api_key:
        return {
            "review": "Error: No OpenAI API key found. Please set it in the .env file.",
            "score": 0
        }

    try:
        # --- Send request to OpenAI ---
        # Use GPT-4-turbo for better reasoning and code understanding
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
                    "role": "user",
                    "content": f"Language: {language}\n\nCode:\n{code}"
                },
            ],
            temperature=0.5,
        )

        # Extract the review text from the response
        review_text = response.choices[0].message.content.strip()

        # Clean and prettify the review text
        review_text = (
            review_text.replace("###", "\n\n###")       # add spacing before headings
                        .replace("####", "\n- **")      # bullet point style for clarity
                        .replace("**:", "**:**")        # fix bold colon spacing
                        .replace("### ", "\n\n### ")    # better readability in frontend
        )

        # Detect rating automatically
        import re
        match = re.search(r'(\d+)\s*out\s*of\s*10', review_text)
        score = int(match.group(1)) 

        return {
            "review": review_text,
            "score": score
        }

    except Exception as e:
        # Handle any errors gracefully
        return {
            "review": f" Error analyzing code: {str(e)}",
            "score": 0
        }


