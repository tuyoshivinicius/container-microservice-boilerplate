import logging

from flask import Flask, request, jsonify

from payment.application.usecases.start_payment_usecase import StartPaymentUseCase, InputDto
from payment.entrypoints.bootstrap.di_container import DIContainer


def create_app() -> "Flask":
    """
    Cria e configura a aplicação Flask com a rota /start-payment.
    """
    app = Flask(__name__)
    container = DIContainer.get_instance()

    @app.route("/start-payment", methods=["POST"])
    def start_payment():
        try:
            payload = request.get_json(force=True)
            input_dto = InputDto(**payload)
            usecase = container.resolve(StartPaymentUseCase)
            result = usecase.execute(input_dto)
            return jsonify({
                "payment_id": result.payment_id,
                "status": result.status
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return app

def run() -> None:
    """
    Inicializa e executa o servidor Flask em modo local.
    """
    logging.info("[INFO] Iniciando servidor Flask (modo local)...")
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
