from payment.application.config.start_payment_config import StartPaymentUseCaseConfigInterface
from payment.infra.config.settings import Settings


class StartPaymentUseCaseConfigAdapter(StartPaymentUseCaseConfigInterface):
    """
    Adaptador para fornecer configurações do caso de uso de início de pagamento
    a partir de uma instância de Settings.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    @property
    def PROCESS_PAYMENT_TOPIC_NAME(self) -> str:
        """Retorna o nome do tópico de processamento de pagamento."""
        return self._settings.PROCESS_PAYMENT_TOPIC_NAME