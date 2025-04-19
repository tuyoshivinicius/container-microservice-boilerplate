from abc import ABC, abstractmethod
from typing import List, Dict
from abc import ABC, abstractmethod
from typing import Optional, List, Dict


class QueueAdapterInterface(ABC):
    @abstractmethod
    def send_message(self, queue_name: str, message: str) -> None:
        """Envia uma mensagem para a fila."""
        ...

    @abstractmethod
    def receive_messages(
        self, 
        queue_name: str, 
        max_messages: int = 10, 
        wait_time: int = 10
    ) -> List[Dict]:
        """Recebe mensagens da fila."""
        ...

    @abstractmethod
    def delete_message(self, queue_name: str, ack_token: str) -> None:
        """Deleta uma mensagem da fila."""
        ...