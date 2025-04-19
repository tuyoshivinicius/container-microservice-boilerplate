from payment.application.usecases.expire_pending_payments_usecase import ExpirePendingPaymentsUseCase
from payment.entrypoints.bootstrap.di_container import DIContainer


def run() -> None:
    """
    Executa o worker responsável por expirar pagamentos pendentes.
    Utiliza o container de injeção de dependências para obter o caso de uso apropriado.
    Em caso de erro, propaga a exceção para que ECS ou logs captem a falha.
    """
    print("[WORKER] Executando expire_pending_payments_worker...")

    container = DIContainer.get_instance()
    usecase = container.resolve(ExpirePendingPaymentsUseCase)

    try:
        expired_count = usecase.execute()
        print(f"[WORKER] Pagamentos expirados: {expired_count}")
    except Exception as e:
        print(f"[ERRO] Falha ao expirar pagamentos: {e}")
        raise
