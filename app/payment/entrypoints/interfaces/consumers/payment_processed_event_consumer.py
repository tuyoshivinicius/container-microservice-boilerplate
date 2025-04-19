import logging
import json

from payment.application.usecases.confirm_payment_usecase import InputDto, ConfirmPaymentUseCase
from payment.entrypoints.bootstrap.di_container import DIContainer
from payment.infra.adapters.sqs_adapter import SqsAdapter
from payment.infra.config.settings import Settings
from payment.infra.monitoring.health_status import HealthStatusMonitor


def run() -> None:
    """
    Consome mensagens da fila SQS, processa cada uma utilizando o caso de uso de confirmação de pagamento,
    gerencia o status de saúde do serviço e registra logs de sucesso ou erro.
    """
    # DI Container
    container = DIContainer.get_instance()
    settings: Settings = container.resolve(Settings)
    sqs_adapter: SqsAdapter = container.resolve(SqsAdapter)
    monitor: HealthStatusMonitor = container.resolve(HealthStatusMonitor)

    # Configuração do monitor de saúde
    monitor.set_healthy()

    queue_url = settings.PAYMENT_PROCESSED_QUEUE_URL

    while True:
        try:
            messages = sqs_adapter.receive_messages(queue_name=queue_url)

            for message in messages:
                try:
                    payload = json.loads(message["Body"])
                    input_dto = InputDto(
                        payment_id=payload["payment_id"],
                        processed_at=payload["processed_at"]
                    )
                    usecase: ConfirmPaymentUseCase = container.resolve(ConfirmPaymentUseCase)
                    result = usecase.execute(input_dto)

                    sqs_adapter.delete_message(
                        queue_name=queue_url,
                        receipt_handle=message["ReceiptHandle"],
                    )
                    logging.info(f"[INFO] Mensagem processada com sucesso: {result}")

                except Exception as e:
                    logging.exception(f"[ERRO] Falha ao processar mensagem: {e}")

        except Exception as critical:
            logging.exception(f"[FATAL] Falha crítica no consumo da fila: {critical}")
            monitor.set_unhealthy()
            break
