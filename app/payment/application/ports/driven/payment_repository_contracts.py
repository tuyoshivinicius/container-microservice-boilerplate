from abc import ABC, abstractmethod
from abc import ABC, abstractmethod

from payment.domain.entities.payment import Payment


class PaymentRepositoryInterface(ABC):
    """
    Interface para repositório de pagamentos.
    Define métodos essenciais para manipulação de pagamentos.
    """

    @abstractmethod
    def find_expired_pending_payments(self) -> list["Payment"]:
        """Retorna uma lista de pagamentos pendentes e expirados."""
        raise NotImplementedError("Método não implementado na interface")

    @abstractmethod
    def save(self, payment: "Payment") -> None:
        """Salva um objeto Payment."""
        raise NotImplementedError("Método não implementado na interface")

    @abstractmethod
    def get_by_id(self, payment_id: int) -> "Payment":
        """Busca um pagamento pelo seu ID."""
        raise NotImplementedError("Método não implementado na interface")