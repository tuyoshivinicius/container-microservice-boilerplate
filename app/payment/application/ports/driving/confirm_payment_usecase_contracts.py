from dataclasses import dataclass
from datetime import datetime
from dataclasses import dataclass
from abc import ABC, abstractmethod
from abc import ABC
from dataclasses import dataclass
from datetime import datetime



@dataclass(frozen=True, slots=True)
class InputDto:
    """
    DTO para informações de pagamento.

    Attributes:
        payment_id (str): Identificador do pagamento.
        processed_at (datetime): Data e hora do processamento.
        amount (float): Valor do pagamento.
        currency (str): Moeda utilizada.
        status (str): Status do pagamento.
        external_reference (str): Referência externa.
        channel (str): Canal de origem do pagamento.
    """
    payment_id: str
    processed_at: datetime
    amount: float
    currency: str
    status: str
    external_reference: str
    channel: str


@dataclass(frozen=True, slots=True)
class OutputDto:
    """
    DTO para saída de operações de pagamento.

    Attributes:
        payment_id (str): Identificador único do pagamento.
        status (str): Estado atual do pagamento.
    """
    payment_id: str
    status: str


class ConfirmPaymentUseCaseInterface(ABC):
    @abstractmethod
    def execute(self, input_dto: 'InputDto') -> 'OutputDto':
        """
        Confirma o pagamento com base nos dados do evento recebido.

        :param input_dto: Dados de entrada para confirmar o pagamento.
        :return: Dados de saída após confirmar o pagamento.
        """
        pass
