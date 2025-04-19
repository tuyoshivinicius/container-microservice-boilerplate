class PaymentMethod:
    """
    Classe que representa um método de pagamento suportado,
    permitindo consultar se suporta parcelamento e se é reembolsável.
    """
    _SUPPORTED_METHODS: dict[str, dict[str, bool]] = {
        "credit_card": {"installments": True,  "refundable": True},
        "pix":         {"installments": False, "refundable": False},
        "boleto":      {"installments": False, "refundable": True},
        "paypal":      {"installments": False, "refundable": True},
    }

    def __init__(self, method: str) -> None:
        if method not in self._SUPPORTED_METHODS:
            raise ValueError(f"Método de pagamento inválido: '{method}'")
        self.value: str = method
        self._properties: dict[str, bool] = self._SUPPORTED_METHODS[method]

    def supports_installments(self) -> bool:
        """Retorna True se o método suporta parcelamento."""
        return self._properties["installments"]

    def is_refundable(self) -> bool:
        """Retorna True se o método é reembolsável."""
        return self._properties["refundable"]

    def __str__(self) -> str:
        return self.value
