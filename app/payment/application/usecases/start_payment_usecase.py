import json

from payment.application.config.start_payment_config import StartPaymentUseCaseConfigInterface
from payment.domain.entities.payment import Payment
from payment.application.ports.driven.topic_adapter_contracts import TopicAdapterInterface
from payment.application.ports.driven.payment_repository_contracts import PaymentRepositoryInterface
from payment.domain.value_objects.payment_method import PaymentMethod
from payment.application.ports.driving.start_payment_usecase_contracts import InputDto, OutputDto, \
    StartPaymentUseCaseInterface


class StartPaymentUseCaseExecuteError(Exception):
    pass



class StartPaymentUseCase(StartPaymentUseCaseInterface):
    """
    Caso de uso para iniciar um pagamento.
    Valida o método de pagamento, cria o pagamento, salva no repositório e publica um evento SNS.
    """

    def __init__(
        self,
        payment_repository: PaymentRepositoryInterface,
        sns_adapter: TopicAdapterInterface,
        config: StartPaymentUseCaseConfigInterface,
    ):
        self._payment_repository = payment_repository
        self._sns_adapter = sns_adapter
        self._config = config

    def execute(self, input_dto: InputDto) -> OutputDto:
        """
        Executa o fluxo de início de pagamento.

        Args:
            input_dto (InputDto): Dados de entrada para iniciar o pagamento.

        Returns:
            OutputDto: Dados de saída com informações do pagamento criado.

        Raises:
            StartPaymentUseCaseExecuteError: Em caso de falha no processo.
        """
        try:
            try:
                payment_method = PaymentMethod(input_dto.payment_method)
            except ValueError:
                raise ValueError(
                    f"Método de pagamento inválido: '{input_dto.payment_method}'"
                )

            payment = Payment.create(
                user_id=input_dto.user_id,
                order_id=input_dto.order_id,
                method=payment_method,
                currency=input_dto.currency_type,
                value=input_dto.value,
            )

            self._payment_repository.save(payment)

            message = {
                "payment_id": payment.id,
                "user_id": payment.user_id,
                "order_id": payment.order_id,
                "payment_method": payment.method.value,
                "currency": payment.currency,
                "value": str(payment.value),
            }

            self._sns_adapter.publish(
                topic_name=self._config.PROCESS_PAYMENT_TOPIC_NAME,
                message=json.dumps(message),
            )

            return OutputDto(
                payment_id=payment.id,
                status=payment.status,
            )

        except Exception as e:
            raise StartPaymentUseCaseExecuteError(
                f"Falha ao iniciar o pagamento: {e}"
            ) from e
