from abc import ABC


class ExpirePendingPaymentsUseCaseInterface(ABC):
    def execute(self) -> None:
        """
        Expira pagamentos pendentes que não foram confirmados após um determinado período.

        :return: None
        """
        raise NotImplementedError("Método não implementado na interface")