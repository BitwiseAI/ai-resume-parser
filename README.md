# AI Resume Parser Agent

This project is an AI-powered resume parser that extracts key information from resumes. It's built with a Python backend using FastAPI and a modern frontend.

## Features

-   **Resume Parsing**: Extracts information like contact details, skills, experience, and education from resumes in various formats (PDF, DOCX).
-   **Structured Output**: Provides the extracted data in a structured JSON format.
-   **Web Interface**: A user-friendly web interface to upload resumes and view the parsed results.
-   **CI/CD**: Continuous integration and deployment pipeline using GitHub Actions.

## Tech Stack

-   **Backend**: Python, FastAPI
-   **Frontend**: HTML, CSS, JavaScript
-   **CI/CD**: GitHub Actions

## Project Structure

```
ai-resume-parser-agent/
├── backend/         # FastAPI backend application
├── frontend/        # Frontend application
├── data/            # Sample resumes and other data
├── tests/           # Tests for the backend
├── deploy/          # Deployment scripts
├── .github/         # GitHub Actions workflows
├── requirements.txt # Python dependencies
└── README.md
```

## Getting Started

### Prerequisites

-   Python 3.8+

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/ai-resume-parser-agent.git
    cd ai-resume-parser-agent
    ```

2.  **Set up the backend:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Start the backend server:**
    ```bash
    uvicorn backend.app.main:app --reload
    ```

2.  Open your browser and navigate to `http://127.0.0.1:8000` to see the application running.

## Usage

-   Navigate to the web interface.
-   Upload a resume file.
-   The parsed information will be displayed on the screen.
