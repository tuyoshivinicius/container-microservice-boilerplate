import pytest
import boto3
import os
import boto3
import pytest
import pytest
import os
import boto3
import pytest
import os
import pytest
import os
import boto3
import pytest
from moto import mock_aws
from payment.entrypoints.bootstrap.di_container import DIContainer
from payment.infra.config.settings import Settings
from payment.infra.models.payment_model import PaymentModel



@pytest.fixture
def create_env_shared() -> None:
    """
    Fixture do pytest que configura variáveis de ambiente necessárias para os testes.
    """
    env_vars = {
        "ENVIRONMENT": "dev",
        "LOG_LEVEL": "INFO",
        "AWS_DEFAULT_REGION": "sa-east-1",
        "PAYMENT_TABLE_NAME": "payment_table",
        "CONSUMER_RUN": "True",
    }
    os.environ.update(env_vars)



@pytest.fixture
def sqs_client() -> boto3.client:
    """
    Fixture do pytest que fornece um cliente SQS simulado usando mock_aws,
    evitando interações reais com a AWS.
    """
    with mock_aws():
        yield boto3.client(
            "sqs",
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        )



@pytest.fixture
def provision_dynamodb_payment_table():
    """
    Fixture para provisionar a tabela DynamoDB utilizada pela PaymentModel.
    """
    with mock_aws():
        # Cria a tabela no DynamoDB simulado, se necessário
        if not PaymentModel.exists():
            PaymentModel.create_table(
                read_capacity_units=5,
                write_capacity_units=5,
                wait=True
            )
        try:
            yield
        finally:
            # Limpa a tabela após os testes
            if PaymentModel.exists():
                PaymentModel.delete_table()


@pytest.fixture
def sns_client() -> boto3.client:
    """
    Fixture para criar o cliente SNS simulado.
    """
    with mock_aws():
        yield boto3.client(
            "sns",
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        )


def custom_delete_message(*args, **kwargs) -> None:
    """
    Exclui uma mensagem de uma fila SQS da AWS e altera a configuração global para interromper o consumidor.

    Args:
        queue_name (str): Nome da fila SQS.
        ack_token (str): Receipt handle da mensagem a ser deletada.
    """

    queue_name = kwargs.get("queue_name")
    ack_token = kwargs.get("ack_token")

    if not queue_name or not ack_token:
        raise ValueError("Os parâmetros 'queue_name' e 'ack_token' são obrigatórios.")

    client = boto3.client("sqs")
    queue_url = client.get_queue_url(QueueName=queue_name)["QueueUrl"]
    client.delete_message(QueueUrl=queue_url, ReceiptHandle=ack_token)

    container = DIContainer.get_instance()
    settings = container.resolve(Settings)
    settings.CONSUMER_RUN = False


@pytest.fixture
def create_custom_delete_message() -> callable:
    """
    Fixture do pytest que fornece o objeto ou função `custom_delete_message`
    para uso em testes.
    """
    yield custom_delete_message
