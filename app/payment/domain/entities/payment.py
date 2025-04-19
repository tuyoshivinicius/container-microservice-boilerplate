from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional
from uuid import uuid4
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4
from typing import Optional

from payment.domain.value_objects.payment_method import PaymentMethod


@dataclass
class Payment:
    id: str
    user_id: str
    order_id: str
    method: 'PaymentMethod'
    currency: str
    value: Decimal
    status: str = field(default="PENDING")
    confirmed_at: Optional[datetime] = field(default=None)
    external_reference: Optional[str] = field(default=None)
    channel: Optional[str] = field(default=None)
    expiration_date: Optional[datetime] = field(default=None)  # útil para o método can_be_expired

    @classmethod
    def create(
        cls,
        user_id: str,
        order_id: str,
        method: 'PaymentMethod',
        currency: str,
        value: Decimal,
        expiration_date: Optional[datetime] = None
    ) -> 'Payment':
        """
        Cria uma nova instância de Payment, gerando um ID único e definindo a data de expiração padrão.
        """
        expiration_date = expiration_date or (datetime.utcnow() + timedelta(minutes=3))
        return cls(
            id=str(uuid4()),
            user_id=user_id,
            order_id=order_id,
            method=method,
            currency=currency,
            value=value,
            status="PENDING",
            expiration_date=expiration_date,
        )

    def approve(self) -> None:
        """Aprova o pagamento."""
        self.status = "APPROVED"

    def fail(self) -> None:
        """Marca o pagamento como falhado."""
        self.status = "FAILED"

    def cancel(self) -> None:
        """Cancela o pagamento."""
        self.status = "CANCELLED"

    def refund(self) -> None:
        """Reembolsa o pagamento."""
        self.status = "REFUNDED"

    def can_be_expired(self) -> bool:
        """
        Verifica se o pagamento pode ser expirado com base no status e na data de expiração.
        """
        return (
            self.status in {"PENDING", "PROCESSING"}
            and self.expiration_date is not None
            and self.expiration_date < datetime.utcnow()
        )

    def expire(self) -> None:
        """
        Expira o pagamento se permitido.
        """
        if not self.can_be_expired():
            raise ValueError("Pagamento não pode ser expirado.")
        self.status = "EXPIRED"

    def confirm(
        self,
        processed_at: datetime,
        external_reference: str,
        channel: str
    ) -> None:
        """
        Confirma o pagamento, registrando data, referência externa e canal.
        """
        if self.status not in {"PENDING", "APPROVED", "PROCESSING"}:
            raise ValueError(f"Status atual não permite confirmação: {self.status}")
        self.status = "CONFIRMED"
        self.confirmed_at = processed_at
        self.external_reference = external_reference
        self.channel = channel
