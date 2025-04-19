import pytest
import os
import json
import pytest
import os
import json
import pytest
import os
import json
import pytest
from typing import Any
import os
import pytest
import json
import os
import pytest

from payment.entrypoints.bootstrap.di_container import DIContainer
from payment.infra.config.settings import Settings


@pytest.fixture
def create_env_start_payment(create_env_shared) -> None:
    """
    Fixture do pytest que configura variáveis de ambiente necessárias
    para o fluxo de início de pagamento nos testes.
    """
    env_vars = {
        "USECASE_EXECUTION": "start_payment",
        "START_PAYMENT_QUEUE_NAME": "start_payment_cmd",
        "PROCESS_PAYMENT_TOPIC_NAME": "process_payment_cmd",
    }
    os.environ.update(env_vars)



@pytest.fixture
def create_start_payment_sqs_queue(sqs_client: Any) -> Any:
    """
    Cria a fila SQS para start payment com configuração de DLQ.
    """
    queue_base_name = os.getenv("START_PAYMENT_QUEUE_NAME")
    dlq_name = f"{queue_base_name}_dlq"

    # Cria a Dead Letter Queue (DLQ)
    dlq_url = sqs_client.create_queue(
        QueueName=dlq_name,
        Attributes={
            "DelaySeconds": "0",
            "MessageRetentionPeriod": "86400",
        },
    )["QueueUrl"]

    # Obtém o ARN da DLQ
    dlq_arn = sqs_client.get_queue_attributes(
        QueueUrl=dlq_url,
        AttributeNames=["QueueArn"]
    )["Attributes"]["QueueArn"]

    # Cria a fila principal com política de redirecionamento para a DLQ
    sqs_client.create_queue(
        QueueName=queue_base_name,
        Attributes={
            "DelaySeconds": "0",
            "MessageRetentionPeriod": "86400",
            "RedrivePolicy": json.dumps({
                "deadLetterTargetArn": dlq_arn,
                "maxReceiveCount": "1"
            }),
        },
    )

    return sqs_client


@pytest.fixture
def create_start_payment_message_success(create_start_payment_sqs_queue) -> None:
    """
    Cria uma mensagem para enviar à fila SQS de início de pagamento.
    """
    message = {
        "user_id": "user_123",
        "order_id": "order_123",
        "payment_method": "credit_card",
        "currency_type": "BRL",
        "value": 100.00,
    }

    queue_name = os.getenv("START_PAYMENT_QUEUE_NAME")
    queue_url = create_start_payment_sqs_queue.get_queue_url(QueueName=queue_name)["QueueUrl"]

    create_start_payment_sqs_queue.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message)
    )


@pytest.fixture
def create_process_payment_sns_topic_and_queue(sns_client, sqs_client):
    """
    Cria o tópico SNS 'process_payment_cmd' e a fila SQS 'process_payment_cmd_test',
    inscrevendo a fila no tópico para receber todas as mensagens.
    """
    # Cria o tópico SNS
    topic_arn = sns_client.create_topic(Name="process_payment_cmd")["TopicArn"]

    # Cria a fila SQS
    queue_url = sqs_client.create_queue(
        QueueName="process_payment_cmd_test",
        Attributes={
            "DelaySeconds": "0",
            "MessageRetentionPeriod": "86400",
        },
    )["QueueUrl"]

    # Obtém o ARN da fila
    queue_arn = sqs_client.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=["QueueArn"]
    )["Attributes"]["QueueArn"]

    # Inscreve a fila no tópico SNS
    sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol="sqs",
        Endpoint=queue_arn
    )

    return topic_arn, queue_url


@pytest.fixture
def create_start_payment_message_fail(create_start_payment_sqs_queue):
    """
    Cria uma mensagem para enviar à fila SQS de início de pagamento.
    """
    message = {
        "user_id": "user_123",
        "order_id": "order_123",
        "payment_method": "xxxxxxx",
        "currency_type": "BRL",
        "value": 100.00,
    }

    queue_name = os.getenv("START_PAYMENT_QUEUE_NAME")
    queue_url = create_start_payment_sqs_queue.get_queue_url(QueueName=queue_name)["QueueUrl"]

    create_start_payment_sqs_queue.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message)
    )

def custom_sleep_finish(seconds: int) -> None:
    """
    Verifica se o valor de `seconds` é igual ao `CONSUMER_WAIT_TIME` nas configurações.
    Se for, define `CONSUMER_RUN` como False.
    """
    settings = DIContainer.get_instance().resolve(Settings)
    if seconds == settings.CONSUMER_WAIT_TIME:
        settings.CONSUMER_RUN = False

@pytest.fixture
def create_custom_sleep_finish() -> callable:
    """
    Fixture do pytest que fornece o objeto ou função `custom_sleep_finish`
    para uso em testes.
    """
    yield custom_sleep_finish
