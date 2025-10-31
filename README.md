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
``` python -m venv venv ```
3. Activate the Virtual Environment
``` venv\Scripts\activate ```
4. Install Dependencies
``` pip install -r requirements.txt ```
5. Create .env file 
- Duplicate the `.env.example` file and rename it as `.env`
``` cp backend/.env.example backend/.env ```
- Add OpenAI API key
``` OPENAI_API_KEY = YOUR_API_KEY ```




