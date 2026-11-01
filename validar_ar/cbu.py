"""Validación de CBU (22 dígitos)."""
from __future__ import annotations

import re

_PESOS_1 = (7, 1, 3, 9, 7, 1, 3)
_PESOS_2 = (3, 9, 7, 1, 3, 9, 7, 1, 3, 9, 7, 1, 3)


def _dv(digitos: str, pesos: tuple) -> int:
    suma = sum(int(d) * p for d, p in zip(digitos, pesos))
    return (10 - suma % 10) % 10


def validar_cbu(valor: str) -> bool:
    """True si el CBU tiene 22 dígitos y ambos dígitos verificadores son correctos."""
    c = re.sub(r"[\s\-]", "", str(valor))
    if not re.fullmatch(r"\d{22}", c):
        return False
    bloque1, bloque2 = c[:8], c[8:]
    return _dv(bloque1[:7], _PESOS_1) == int(bloque1[7]) and \
        _dv(bloque2[:13], _PESOS_2) == int(bloque2[13])


def banco_y_sucursal(valor: str) -> tuple:
    """Devuelve (código de entidad, código de sucursal) de un CBU válido."""
    if not validar_cbu(valor):
        raise ValueError(f"CBU inválido: {valor!r}")
    c = re.sub(r"[\s\-]", "", str(valor))
    return c[:3], c[3:7]
