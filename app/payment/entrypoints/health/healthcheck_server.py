from flask import Flask, jsonify

from payment.infra.monitoring.health_status import HealthStatusMonitor


def create_healthcheck_app() -> Flask:
    """
    Cria e retorna uma aplicação Flask com um endpoint '/healthz' para checagem de saúde.
    Utiliza um monitor singleton (HealthStatusMonitor) para determinar o status do sistema.
    """
    app = Flask(__name__)
    monitor = HealthStatusMonitor.instance()

    @app.route("/healthz", methods=["GET"])
    def healthcheck():
        status = monitor.get_status()
        http_status = 200 if status == "healthy" else 503
        return jsonify({"status": status}), http_status

    return app
