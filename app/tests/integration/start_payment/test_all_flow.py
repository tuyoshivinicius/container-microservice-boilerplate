import time
from unittest.mock import patch
from payment.entrypoints.bootstrap.di_container import DIContainer
from payment.infra.adapters.sqs_adapter import SqsAdapter


def test_should_succeed_when_starting_new_processing(
    create_env_start_payment,
    create_start_payment_message_success,
    provision_dynamodb_payment_table,
    create_process_payment_sns_topic_and_queue,
    create_custom_delete_message
) -> None:
    """
    Testa se o fluxo de pagamento funciona corretamente ao iniciar um novo processamento.
    """
    # ARRANGE
    container = DIContainer.get_instance()
    sqs_adapter = container.resolve(SqsAdapter)

    # ACT
    with patch.object(SqsAdapter, "delete_message", side_effect=create_custom_delete_message):
        from main import main
        result = main()

    # ASSERT
    messages = sqs_adapter.receive_messages(
        queue_name="process_payment_cmd_test",
        max_messages=1,
        wait_time=0
    )
    assert len(messages) == 1



def test_should_fail_when_starting_new_processing_with_invalid_payment_method(
    create_env_start_payment,
    create_start_payment_message_fail,
    provision_dynamodb_payment_table,
    create_process_payment_sns_topic_and_queue,
    create_custom_sleep_finish
) -> None:
    """
    Testa se o fluxo de pagamento falha ao iniciar um novo processamento com método de pagamento inválido.
    """
    # ARRANGE
    container = DIContainer.get_instance()
    sqs_adapter = container.resolve(SqsAdapter)

    # ACT
    with patch.object(time, "sleep", side_effect=create_custom_sleep_finish):
        from main import main
        main()

    # ASSERT
    messages = sqs_adapter.receive_messages(
        queue_name="process_payment_cmd_test",
        max_messages=1,
        wait_time=0
    )
    assert not messages
