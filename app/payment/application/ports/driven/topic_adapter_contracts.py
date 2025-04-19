from abc import ABC, abstractmethod
from abc import ABC


class TopicAdapterInterface(ABC):
    """
    Interface abstrata para adaptadores de tópicos.
    Exige a implementação do método 'publish' para publicar mensagens em um tópico específico.
    """

    @abstractmethod
    def publish(self, topic_name: str, message: str) -> None:
        """
        Publica uma mensagem em um tópico específico.

        :param topic_name: Nome do tópico.
        :param message: Mensagem a ser publicada.
        """
        pass