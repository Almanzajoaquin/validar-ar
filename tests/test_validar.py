import pytest
from validar_ar import (banco_y_sucursal, formatear_cuit, generar_cuit,
                        validar_cbu, validar_cuit, validar_dni)
from validar_ar.cbu import _PESOS_1, _PESOS_2, _dv
from validar_ar.cli import main


def test_cuit_valido_conocido():
    assert validar_cuit("30-50001091-2")  # Banco de la Nación Argentina
    assert validar_cuit("30500010912")


def test_cuit_invalido():
    assert not validar_cuit("30-50001091-3")
    assert not validar_cuit("12-34567890-1")
    assert not validar_cuit("abc")
    assert not validar_cuit("")


def test_formatear():
    assert formatear_cuit("30500010912") == "30-50001091-2"
    with pytest.raises(ValueError):
        formatear_cuit("123")


@pytest.mark.parametrize("dni", range(10_000_000, 10_000_300))
@pytest.mark.parametrize("sexo", ["M", "F", "X"])
def test_generar_siempre_valido(dni, sexo):
    assert validar_cuit(generar_cuit(dni, sexo))


def test_generar_dni_corto():
    assert validar_cuit(generar_cuit("5123456", "M"))


def test_generar_errores():
    with pytest.raises(ValueError):
        generar_cuit("abc", "M")
    with pytest.raises(ValueError):
        generar_cuit("12345678", "Z")


def _cbu_valido():
    b1 = "0110012"
    b2 = "0000123456789"
    return b1 + str(_dv(b1, _PESOS_1)) + b2 + str(_dv(b2, _PESOS_2))


def test_cbu():
    c = _cbu_valido()
    assert validar_cbu(c)
    assert banco_y_sucursal(c) == ("011", "0012")
    malo = c[:-1] + str((int(c[-1]) + 1) % 10)
    assert not validar_cbu(malo)
    assert not validar_cbu("123")


def test_dni():
    assert validar_dni("12.345.678")
    assert validar_dni(5123456)
    assert not validar_dni("123")
    assert not validar_dni("0000000")


def test_cli(capsys):
    assert main(["cuit", "30-50001091-2"]) == 0
    assert main(["cuit", "30-50001091-9"]) == 1
    assert main(["generar", "12345678", "M"]) == 0
    assert "20-12345678" in capsys.readouterr().out
