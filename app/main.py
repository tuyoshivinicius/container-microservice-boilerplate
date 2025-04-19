import os
import os

from payment.entrypoints.interfaces.api import rest_api
from payment.entrypoints.interfaces.consumers import (
    start_payment_command_consumer,
    payment_processed_event_consumer,
)

from payment.entrypoints.interfaces.api.rest_api import create_app

app = create_app() if os.getenv("USECASE_EXECUTION") == "rest_api" else None


def main() -> None:
    """
    Executa a estratégia definida pela variável de ambiente USECASE_EXECUTION.
    """
    usecase_execution = os.getenv("USECASE_EXECUTION")

    strategies = {
        "start_payment": start_payment_command_consumer.run,
        "confirm_payment": payment_processed_event_consumer.run,
        "rest_api": rest_api.run,
    }

    strategy = strategies.get(usecase_execution)
    if not strategy:
        raise ValueError(f"USECASE_EXECUTION inválido: {usecase_execution!r}")

    strategy()
