from payment.application.ports.driven.payment_repository_contracts import PaymentRepositoryInterface


class ExpirePendingPaymentsUseCase:
    def __init__(self, payment_repository: 'PaymentRepositoryInterface'):
        self.__payment_repository = payment_repository

    def execute(self) -> int:
        """
        Expira pagamentos pendentes que já venceram.

        Retorna:
            int: Quantidade de pagamentos expirados.
        """
        expired_candidates = self.__payment_repository.find_expired_pending_payments()
        count = 0

        for payment in expired_candidates:
            if payment.can_be_expired():
                payment.expire()
                self.__payment_repository.save(payment)
                count += 1

        return count
