"""Interfaz de línea de comandos: validar-ar."""
from __future__ import annotations

import argparse
import sys

from . import (__version__, formatear_cuit, generar_cuit, validar_cbu,
               validar_cuit, validar_dni)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="validar-ar",
                                description="Valida CUIT/CUIL, CBU y DNI argentinos.")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    for nombre in ("cuit", "cbu", "dni"):
        s = sub.add_parser(nombre, help=f"validar un {nombre.upper()}")
        s.add_argument("valor")

    g = sub.add_parser("generar", help="generar CUIL/CUIT a partir de un DNI")
    g.add_argument("dni")
    g.add_argument("sexo", choices=["M", "F", "X", "m", "f", "x"])

    a = p.parse_args(argv)

    if a.cmd == "generar":
        try:
            print(generar_cuit(a.dni, a.sexo))
            return 0
        except ValueError as e:
            print(e, file=sys.stderr)
            return 2

    validador = {"cuit": validar_cuit, "cbu": validar_cbu, "dni": validar_dni}[a.cmd]
    ok = validador(a.valor)
    if ok and a.cmd == "cuit":
        print(f"✔ válido: {formatear_cuit(a.valor)}")
    else:
        print("✔ válido" if ok else "✘ inválido")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
