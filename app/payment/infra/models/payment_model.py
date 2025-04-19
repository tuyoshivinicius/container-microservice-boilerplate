import os

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, MapAttribute

TABLE_NAME = os.getenv("PAYMENT_TABLE_NAME", "payment_table")
REGION = os.getenv("AWS_DEFAULT_REGION", "sa-east-1")

class PaymentMethodAttribute(MapAttribute):
    """
    Representa atributos de um método de pagamento.

    Campos:
        name (str): Nome do método de pagamento (obrigatório).
        metadata (str, opcional): Metadados adicionais (pode ser nulo).
    """
    name: str = UnicodeAttribute()
    metadata: str | None = UnicodeAttribute(null=True)


class PaymentModel(Model):
    """
    Modelo de pagamento para armazenamento em DynamoDB.
    """
    class Meta:
        table_name = TABLE_NAME
        region = REGION

    id: str = UnicodeAttribute(hash_key=True)
    user_id: str = UnicodeAttribute()
    order_id: str = UnicodeAttribute()
    method: PaymentMethodAttribute = PaymentMethodAttribute()
    currency: str = UnicodeAttribute()
    value: float = NumberAttribute()
    status: str = UnicodeAttribute(default="PENDING")
