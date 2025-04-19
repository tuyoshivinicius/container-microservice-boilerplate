from decimal import Decimal
from typing import Optional
from payment.domain.entities.payment import Payment
from payment.domain.value_objects.payment_method import PaymentMethod
from payment.infra.models.payment_model import PaymentModel


class PaymentRepository:
    """
    Repositório para operações de persistência de pagamentos.
    """

    def save(self, payment: Payment) -> None:
        """
        Salva um objeto Payment no banco de dados.
        """
        PaymentModel(
            id=payment.id,
            user_id=payment.user_id,
            order_id=payment.order_id,
            method={
                "name": payment.method.value,
                "metadata": getattr(payment.method, "metadata", None)
            },
            currency=payment.currency,
            value=payment.value,
            status=payment.status
        ).save()

    def get_by_id(self, payment_id: str) -> Optional[Payment]:
        """
        Recupera um Payment pelo ID. Retorna None se não encontrado.
        """
        try:
            item = PaymentModel.get(payment_id)
            method = PaymentMethod(item.method["name"])
            return Payment(
                id=item.id,
                user_id=item.user_id,
                order_id=item.order_id,
                method=method,
                currency=item.currency,
                value=Decimal(str(item.value)),
                status=item.status
            )
        except PaymentModel.DoesNotExist:
            return None
