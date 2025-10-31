# AI-Powered Code Review Assistant
This project is a full-stack web application that allows users to paste code in various programming languages and receive AI-generated feedback with a quality score. 
It uses Flask (Python) for the backend, OpenAI's GPT model for code analysis, and HTML/CSS for the frontend server directly from Flask.

## Technologies used
- Frontend: HTML, CSS, JavaScript
- Backend: Flask (Python)
- Database: SQLite (via SQLAlchemy)
- AI Model: OpenAI GPT-4o-mini
- Environment: Python

## Features
- Code snippets submitted for AI-based review.
- Instant feedback with clarity, readability, and efficiency analysis received.
- Score out of 10 given to code.
- Previous reviews stored in the database.
- Individual reviews can be deleted.
- For testing purposes -> bulk delete.
- Responsice UI

## Setup Instructions
1. Cloning the Repository
```
git clone https://github.com/Mini1521/ai-code-reviewer.git
cd ai-code-reviewer
```
2. Creating a Virtual Environment
``` 
python -m venv venv 
```
3. Activate the Virtual Environment
```
venv\Scripts\activate 
```
4. Install Dependencies
``` 
pip install -r requirements.txt 
```
5. Create .env file 
- Duplicate the `.env.example` file and rename it as `.env`
```
cp backend/.env.example backend/.env
```
- Add OpenAI API key
```
OPENAI_API_KEY = YOUR_API_KEY
```

## How to run the application
Start the Flask backend
```
cd backend 
python app.py
```
Once it starts, Flask will serve both the API and the frontend. The app runs locally on: `http://127.0.0.1:5000/` \
*(You do not need to use VS Code Live Server. The HTML `index.html` is served directly from the Flask backend.)*

## API Endpoints
- POST `/api/review`: Submit code for AI review
- GET `/api/reviews`: Fetch all stored reviews
- GET `/api/review/<id>`: Get a specific review by ID
- DELETE `/api/review/<id>`: Delete a specific review

## Assumptions Made
- The frontend `index.html` is served from Flask, not opened manually or via Live Server.
- The OpenAI API key is available and valid in the `.env` file.
- Users input syntactically valid code.
- The backend and frontend run locally on the same machine, `http://127.0.0.1:5000/`.
- SQLite is used for simplicity and requires no manual configuration.

## Testing the API
- A test script is included in `backend/tests/test_routes.py`
- To run `python backenc/tests/test_routes.py`
- This script:
  - Posts sample reviews for multiple languages.
  - Retrieves all reviews.
  - Deletes individual or all reviews (bulk delete for cleanup).

### Total time spent on the project: 10 hours.
