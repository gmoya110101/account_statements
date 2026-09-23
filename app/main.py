"""Main entry point for the application."""

from dotenv import load_dotenv

from app.project_app.use_cases.executor import main

load_dotenv()

if __name__ == "__main__":
    main()