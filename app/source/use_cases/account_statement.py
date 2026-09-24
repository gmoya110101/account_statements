"""Executor use case for processing jobs."""

import argparse

from dotenv import load_dotenv

from app.source.app_settings import settings
from app.source.repositories.processors.executors.account_statement.job import (
    AccountStatementJob,
)

load_dotenv()

parser = argparse.ArgumentParser(
    description="Executes Account Statement Executor job.",
)

def main() -> None:
    """Main function for the executor use case."""
    grafana_url = settings.grafana.URL
    grafana_token = settings.grafana.TOKEN

    telegram_base_url = settings.telegram.URL
    telegram_endpoint = settings.telegram.ENDPOINT
    telegram_token = settings.telegram.TOKEN
    telegram_message= settings.telegram.MESSAGE

    debtors = settings.global_vars.DEBTORS

    job = AccountStatementJob(
        settings={
            "downloader": {
                "url": grafana_url,
                "token": grafana_token,
            },
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
    """Execute the account statement job."""
    main()