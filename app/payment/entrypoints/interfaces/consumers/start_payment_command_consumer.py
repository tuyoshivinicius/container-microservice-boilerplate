import logging
import json
import time

from payment.application.ports.driving.start_payment_usecase_contracts import InputDto
from payment.application.usecases.start_payment_usecase import StartPaymentUseCase, StartPaymentUseCaseExecuteError
from payment.entrypoints.bootstrap.di_container import DIContainer
from payment.infra.adapters.sqs_adapter import SqsAdapter
from payment.infra.config.settings import Settings
from payment.infra.monitoring.health_status import HealthStatusMonitor


def run() -> None:
    """
    Consome mensagens de uma fila SQS, processa cada mensagem utilizando o caso de uso StartPaymentUseCase,
    e gerencia o status de saúde do serviço.
    """
    # DI Container
    container = DIContainer.get_instance()
    settings: Settings = container.resolve(Settings)
    sqs_adapter: SqsAdapter = container.resolve(SqsAdapter)
    monitor: HealthStatusMonitor = container.resolve(HealthStatusMonitor)

    # Configuração do monitor de saúde
    monitor.set_healthy()

    while settings.CONSUMER_RUN:
        try:
            messages = sqs_adapter.receive_messages(
                queue_name=settings.START_PAYMENT_QUEUE_NAME
            )

            if not messages:
                logging.info("[INFO] Nenhuma mensagem recebida.")
                time.sleep(settings.CONSUMER_WAIT_TIME)
                continue

            usecase: StartPaymentUseCase = container.resolve(StartPaymentUseCase)

            for message in messages:
                try:
                    payload = json.loads(message["Body"])
                    input_dto = InputDto(**payload)
                    result = usecase.execute(input_dto)

                    sqs_adapter.delete_message(
                        queue_name=settings.START_PAYMENT_QUEUE_NAME,
                        ack_token=message["ReceiptHandle"],
                    )
                except StartPaymentUseCaseExecuteError as e:
                    logging.exception(f"[ERRO] Falha ao processar mensagem: {e}")

        except Exception as e:
            logging.exception(f"[FATAL] Falha crítica no consumo da fila: {e}")
            monitor.set_unhealthy()
            raise
