from punq import Container

class DIContainer:
    """
    Singleton para o container de injeção de dependências.
    Responsável por registrar e fornecer instâncias dos componentes do domínio de pagamentos.
    """
    _instance: "Container | None" = None

    @classmethod
    def get_instance(cls) -> "Container":
        """
        Retorna a instância única do container, criando-a se necessário.
        """
        if cls._instance is None:
            cls._instance = cls._create_container()
        return cls._instance

    @classmethod
    def _create_container(cls) -> "Container":
        """
        Cria e registra todas as dependências e implementações necessárias no container.
        """
        from payment.application.config.start_payment_config import StartPaymentUseCaseConfigInterface
        from payment.application.ports.driven.payment_repository_contracts import PaymentRepositoryInterface
        from payment.application.ports.driven.queue_adapter_contracts import QueueAdapterInterface
        from payment.application.ports.driven.topic_adapter_contracts import TopicAdapterInterface
        from payment.application.usecases.confirm_payment_usecase import ConfirmPaymentUseCase
        from payment.application.usecases.expire_pending_payments_usecase import ExpirePendingPaymentsUseCase
        from payment.application.usecases.start_payment_usecase import StartPaymentUseCase
        from payment.infra.adapters.sns_adapter import SnsAdapter
        from payment.infra.adapters.sqs_adapter import SqsAdapter
        from payment.infra.adapters.start_payment_usecase_config_adapter import StartPaymentUseCaseConfigAdapter
        from payment.infra.config.settings import Settings
        from payment.infra.models.payment_model import PaymentModel
        from payment.infra.monitoring.health_status import HealthStatusMonitor
        from payment.infra.repositories.payment_repository import PaymentRepository

        container = Container()

        # Registro das implementações e instâncias
        container.register(Settings, instance=Settings())
        container.register(HealthStatusMonitor, singleton=True)
        container.register(StartPaymentUseCaseConfigInterface, StartPaymentUseCaseConfigAdapter)
        container.register(StartPaymentUseCaseConfigAdapter)
        container.register(PaymentModel)
        container.register(PaymentRepositoryInterface, PaymentRepository)
        container.register(PaymentRepository)
        container.register(TopicAdapterInterface, SnsAdapter)
        container.register(QueueAdapterInterface, SqsAdapter)
        container.register(SqsAdapter)

        # Casos de uso com dependências resolvidas automaticamente
        container.register(StartPaymentUseCase)
        container.register(ConfirmPaymentUseCase)
        container.register(ExpirePendingPaymentsUseCase)

        return container