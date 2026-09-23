"""Executor use case for processing jobs."""

from app.project_app.app_settings import settings
from app.project_app.repositories.processors.executor.job import ExecutorJob


def main() -> None:
    """Main function for the executor use case."""
    grafana_url = settings.grafana.URL
    grafana_token = settings.grafana.TOKEN

    telegram_base_url = settings.telegram.URL
    telegram_endpoint = settings.telegram.ENDPOINT
    telegram_token = settings.telegram.TOKEN
    telegram_message= settings.telegram.MESSAGE

    job = ExecutorJob(
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
    job.execute(debtors=[
                {"name": "Gerardo", "chat_id": "6113056518"},
            ])
