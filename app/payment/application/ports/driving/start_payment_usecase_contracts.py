from dataclasses import dataclass
from dataclasses import dataclass
from decimal import Decimal
from _pydecimal import Decimal
from abc import ABC, abstractmethod
from dataclasses import dataclass



@dataclass(frozen=True, slots=True)
class InputDto:
    """
    DTO para informações de transação de pagamento.

    Atributos:
        user_id (str): Identificador do usuário.
        order_id (str): Identificador do pedido.
        payment_method (str): Método de pagamento utilizado.
        currency_type (str): Tipo de moeda da transação.
        value (Decimal): Valor da transação.
    """
    user_id: str
    order_id: str
    payment_method: str
    currency_type: str
    value: Decimal


@dataclass(frozen=True, slots=True)
class OutputDto:
    """
    DTO para saída de operação de pagamento.

    Attributes:
        payment_id (str): Identificador do pagamento.
        status (str): Status do pagamento.
    """
    payment_id: str
    status: str


class StartPaymentUseCaseInterface(ABC):

    @abstractmethod
    def execute(self, input_dto: InputDto) -> OutputDto:
        """
        Inicia o processo de pagamento.

        :param input_dto: Dados de entrada para iniciar o pagamento.
        :return: Dados de saída após iniciar o pagamento.
        """
        raise NotImplementedError("Método não implementado na interface")
