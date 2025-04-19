from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """
    Classe de configuração centralizada para variáveis de ambiente e parâmetros
    relacionados à aplicação de pagamentos e integração com AWS.
    """

    # SHARED
    ENVIRONMENT: str = Field("dev", description="Ambiente da aplicação")
    LOG_LEVEL: str = Field("INFO", description="Nível de log")
    AWS_DEFAULT_REGION: str = Field("sa-east-1", description="Região padrão da AWS")
    PAYMENT_TABLE_NAME: str = Field("payment_table", description="Nome da tabela de pagamentos")
    CONSUMER_RUN: bool = Field(True, description="Executa o consumidor de eventos")
    CONSUMER_WAIT_TIME: int = Field(5, description="Tempo de espera entre as tentativas de leitura da fila SQS")

    # START PAYMENT
    START_PAYMENT_QUEUE_NAME: Optional[str] = Field(None, description="Nome da fila SQS 'start_payment_cmd'")
    PROCESS_PAYMENT_TOPIC_NAME: Optional[str] = Field(None, description="Nome do tópico SNS 'payment_started_evt'")

    # CONFIRM PAYMENT
    PAYMENT_PROCESSED_QUEUE_NAME: Optional[str] = Field(None, description="Nome da fila SQS 'payment_processed_evt'")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }
