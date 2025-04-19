from abc import ABC, abstractmethod
from dataclasses import dataclass
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class StartPaymentUseCaseConfigInterface(ABC):
    """
    Interface de configuração para o caso de uso de início de pagamento.
    Exige que subclasses implementem a propriedade PROCESS_PAYMENT_TOPIC_NAME.
    """

    @property
    @abstractmethod
    def PROCESS_PAYMENT_TOPIC_NAME(self) -> str:
        """Nome do tópico de processamento de pagamento."""
        raise NotImplementedError("Método não implementado na interface")
