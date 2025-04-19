from payment.application.ports.driving.confirm_payment_usecase_contracts import OutputDto, InputDto
from payment.application.ports.driven.payment_repository_contracts import PaymentRepositoryInterface


class ConfirmPaymentUseCase:
    """
    Classe responsável por confirmar um pagamento, garantindo idempotência e validando regras de negócio antes de atualizar o status do pagamento.
    """

    def __init__(self, payment_repository: PaymentRepositoryInterface):
        self._payment_repository = payment_repository

    def execute(self, input_dto: InputDto) -> OutputDto:
        """
        Confirma o pagamento se todas as regras de negócio forem atendidas.

        Args:
            input_dto (InputDto): Dados de entrada para confirmação do pagamento.

        Returns:
            OutputDto: Resultado da confirmação do pagamento.

        Raises:
            ValueError: Se alguma regra de negócio não for atendida.
        """
        payment = self._payment_repository.get_by_id(input_dto.payment_id)

        # Idempotência: se já confirmado, retorna imediatamente
        if payment.status == "confirmed":
            return OutputDto(payment_id=payment.id, status=payment.status)

        # Validação do status do evento recebido
        if input_dto.status.strip().upper() != "APPROVED":
            raise ValueError(f"Status do evento inválido para confirmação: {input_dto.status}")

        # Validação do status atual do pagamento
        if payment.status not in {"pending", "processed"}:
            raise ValueError(f"Estado do pagamento não permite confirmação: {payment.status}")

        # Validação de valor e moeda
        if payment.amount != input_dto.amount or payment.currency != input_dto.currency:
            raise ValueError("Valor ou moeda do evento não conferem com o pagamento")

        # Confirma o pagamento com base nos dados do evento
        payment.confirm(
            processed_at=input_dto.processed_at,
            external_reference=input_dto.external_reference,
            channel=input_dto.channel
        )

        self._payment_repository.save(payment)

        return OutputDto(payment_id=payment.id, status=payment.status)
