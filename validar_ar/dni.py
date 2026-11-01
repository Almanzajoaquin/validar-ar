"""Validación básica de DNI."""
from __future__ import annotations

import re


def validar_dni(valor: str | int) -> bool:
    """True si es un DNI plausible: 7 u 8 dígitos (admite puntos)."""
    d = re.sub(r"[\s.]", "", str(valor))
    return bool(re.fullmatch(r"\d{7,8}", d)) and int(d) > 0
