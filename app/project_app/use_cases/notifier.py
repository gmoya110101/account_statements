import argparse

from dotenv import load_dotenv

from app.project_app.app_settings import settings
from app.project_app.repositories.processors.executors.notifier.job import (
    NotifierJob,
)

load_dotenv()

parser = argparse.ArgumentParser(
    description="Executes Notifier job.",
)

def main() -> None:
    """Main function for the executor use case."""

    telegram_base_url = settings.telegram.URL
    telegram_endpoint = settings.telegram.ENDPOINT
    telegram_token = settings.telegram.TOKEN
    telegram_message= settings.telegram.MESSAGE

    debtors = settings.global_vars.DEBTORS

    job = NotifierJob(
        settings={
            "sender": {
                "base_url": telegram_base_url,
                "endpoint": telegram_endpoint,
                "token": telegram_token,
                "message": telegram_message,
            },
        }
    )
    job.execute(debtors=debtors)

if __name__ == "__main__":
    """Execute the notifier job."""
    main()