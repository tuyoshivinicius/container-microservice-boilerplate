import boto3
import logging
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from payment.application.ports.driven.topic_adapter_contracts import TopicAdapterInterface

class SnsAdapter(TopicAdapterInterface):
    """
    Adaptador para publicação de mensagens em tópicos SNS da AWS.
    """

    def __init__(self, sns_client=None) -> None:
        self._sns = sns_client or boto3.client("sns")

    def publish(self, topic_name: str, message: str) -> None:
        """
        Publica uma mensagem em um tópico SNS identificado pelo nome.

        :param topic_name: Nome do tópico SNS.
        :param message: Mensagem a ser publicada.
        :raises ValueError: Se o tópico não for encontrado.
        :raises BotoCoreError, ClientError: Em caso de erro na AWS.
        """
        try:
            topic_arn = self._get_topic_arn(topic_name)
            if not topic_arn:
                raise ValueError(f"Tópico SNS '{topic_name}' não encontrado.")
            self._sns.publish(TopicArn=topic_arn, Message=message)
        except (BotoCoreError, ClientError):
            raise

    def _get_topic_arn(self, name: str) -> str | None:
        """
        Busca o ARN do tópico SNS cujo nome contém o valor informado.

        :param name: Nome do tópico SNS.
        :return: ARN do tópico ou None se não encontrado.
        """
        topics = self._sns.list_topics().get("Topics", [])
        return next((t["TopicArn"] for t in topics if name in t["TopicArn"]), None)
