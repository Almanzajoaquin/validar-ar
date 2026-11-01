"""Validación y generación de CUIT/CUIL argentinos."""
from __future__ import annotations

import re

_PESOS = (5, 4, 3, 2, 7, 6, 5, 4, 3, 2)
PREFIJOS_VALIDOS = {"20", "23", "24", "27", "30", "33", "34"}


def limpiar(valor: str) -> str:
    """Quita guiones, puntos y espacios."""
    return re.sub(r"[\s.\-]", "", str(valor))


def _digito_verificador(base10: str) -> int:
    suma = sum(int(d) * p for d, p in zip(base10, _PESOS))
    r = 11 - (suma % 11)
    return 0 if r == 11 else r  # 10 => combinación inválida


def validar_cuit(valor: str) -> bool:
    """Devuelve True si el CUIT/CUIL es válido (formato, prefijo y dígito)."""
    c = limpiar(valor)
    if not re.fullmatch(r"\d{11}", c):
        return False
    if c[:2] not in PREFIJOS_VALIDOS:
        return False
    dv = _digito_verificador(c[:10])
    return dv != 10 and dv == int(c[10])


def formatear_cuit(valor: str) -> str:
    """Devuelve el CUIT con formato XX-XXXXXXXX-X. Lanza ValueError si es inválido."""
    if not validar_cuit(valor):
        raise ValueError(f"CUIT inválido: {valor!r}")
    c = limpiar(valor)
    return f"{c[:2]}-{c[2:10]}-{c[10]}"


def generar_cuit(dni: str | int, sexo: str) -> str:
    """Genera el CUIL/CUIT de una persona a partir de su DNI.

    sexo: 'M' (prefijo 20), 'F' (prefijo 27) o 'X' (prefijo 24).
    Si el dígito da 10, se usa el prefijo 23, como en la práctica oficial.
    """
    d = limpiar(str(dni)).zfill(8)
    if not re.fullmatch(r"\d{8}", d):
        raise ValueError(f"DNI inválido: {dni!r}")
    sexo = sexo.upper()
    if sexo not in {"M", "F", "X"}:
        raise ValueError("sexo debe ser 'M', 'F' o 'X'")
    prefijo = {"M": "20", "F": "27", "X": "24"}[sexo]
    dv = _digito_verificador(prefijo + d)
    if dv == 10:
        prefijo = "23"
        dv = _digito_verificador(prefijo + d)
    return f"{prefijo}-{d}-{dv}"
