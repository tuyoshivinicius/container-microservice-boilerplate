import boto3
import boto3
import logging
from botocore.exceptions import BotoCoreError, ClientError
from payment.application.ports.driven.queue_adapter_contracts import QueueAdapterInterface


class SqsAdapter(QueueAdapterInterface):
    """
    Adaptador para operações com AWS SQS.
    """

    def __init__(self, sqs_client=None) -> None:
        self._sqs = sqs_client or boto3.client("sqs")

    def send_message(self, queue_name: str, message: str) -> None:
        """
        Envia uma mensagem para a fila SQS especificada.
        """
        try:
            queue_url = self._get_queue_url(queue_name)
            self._sqs.send_message(QueueUrl=queue_url, MessageBody=message)
        except (BotoCoreError, ClientError) as e:
            raise e

    def receive_messages(
        self, queue_name: str, max_messages: int = 1, wait_time: int = 5
    ) -> list[dict]:
        """
        Recebe mensagens da fila SQS especificada.
        """
        try:
            queue_url = self._get_queue_url(queue_name)
            response = self._sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time,
                MessageAttributeNames=["All"],
            )
            return response.get("Messages", [])
        except (BotoCoreError, ClientError):
            return []

    def delete_message(self, queue_name: str, ack_token: str) -> None:
        """
        Exclui uma mensagem da fila SQS usando o ReceiptHandle.
        """
        try:
            queue_url = self._get_queue_url(queue_name)
            self._sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=ack_token)
        except (BotoCoreError, ClientError) as e:
            raise e

    def _get_queue_url(self, name: str) -> str:
        """
        Recupera a URL da fila SQS pelo nome.
        """
        return self._sqs.get_queue_url(QueueName=name)["QueueUrl"]
