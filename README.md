# validar-ar 🇦🇷

Librería y CLI en Python, **sin dependencias**, para validar y generar documentos argentinos:

- **CUIT / CUIL**: validación (formato, prefijo, dígito verificador), formateo y generación desde DNI
- **CBU**: validación de los dos dígitos verificadores y extracción de banco/sucursal
- **DNI**: validación básica de formato

## Instalación

```bash
pip install git+https://github.com/Almanzajoaquin/validar-ar.git
```

## Uso como librería

```python
from validar_ar import validar_cuit, formatear_cuit, generar_cuit, validar_cbu

validar_cuit("30-50001091-2")      # True
formatear_cuit("30500010912")      # '30-50001091-2'
generar_cuit("12345678", "M")      # '20-12345678-6'
validar_cbu("0110012900001234567891")  # True
```

## Uso desde la terminal

```bash
validar-ar cuit 30-50001091-2
validar-ar cbu 0110012900001234567891
validar-ar dni 12.345.678
validar-ar generar 12345678 M
```

El código de salida es `0` si es válido y `1` si no, así que sirve en scripts.

## Tests

```bash
pip install pytest && pytest
```

## Contribuir

¡Los PRs son bienvenidos! Ideas: validación de CUIT por tipo de persona, tabla de códigos de bancos, soporte para alias de CBU, empaquetado en npm/JS.

## Licencia

MIT
