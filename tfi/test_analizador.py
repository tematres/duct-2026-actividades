"""
test_analizador.py

Pruebas unitarias con pytest para la función `contar_frecuencias`
(definida en analizador.py).

Casos cubiertos:
1. Caso básico: conteo correcto sobre una lista de tokens con repeticiones.
2. Texto vacío: una lista vacía de tokens devuelve un diccionario vacío
   (y `tokenizar("")` no produce tokens).
3. Mayúsculas y minúsculas: "Hola", "hola", "HOLA", etc. se cuentan
   como la misma palabra (gracias a `tokenizar`, que pasa todo a minúsculas).
4. (Extra) Filtrado de stopwords con `sin_stopwords=True`.

Cómo ejecutar:
    pytest -v test_analizador.py

Requisitos:
- `analizador.py` y `ejercicio_2.py` en el mismo directorio que este test.
- matplotlib instalado (por el import a nivel de módulo en analizador.py).
"""

import pytest

from analizador import contar_frecuencias, tokenizar


# ---------------------------------------------------------------------------
# 1) Caso básico
# ---------------------------------------------------------------------------
def test_conteo_basico():
    """Cuenta correctamente las repeticiones de cada palabra."""
    tokens = ["hola", "mundo", "hola", "python", "hola", "mundo"]

    resultado = contar_frecuencias(tokens)

    assert resultado == {"hola": 3, "mundo": 2, "python": 1}


@pytest.mark.parametrize(
    "tokens, esperado",
    [
        (["a"], {"a": 1}),
        (["a", "a", "a"], {"a": 3}),
        (["x", "y", "z"], {"x": 1, "y": 1, "z": 1}),
        (["uno", "dos", "uno", "tres", "dos", "uno"], {"uno": 3, "dos": 2, "tres": 1}),
    ],
)
def test_conteo_basico_parametrizado(tokens, esperado):
    """Variantes del caso básico con distintos patrones de repetición."""
    assert contar_frecuencias(tokens) == esperado


# ---------------------------------------------------------------------------
# 2) Texto vacío
# ---------------------------------------------------------------------------
def test_texto_vacio_lista_de_tokens():
    """Una lista vacía de tokens produce un diccionario vacío."""
    resultado = contar_frecuencias([])

    assert resultado == {}
    assert len(resultado) == 0


def test_texto_vacio_desde_string():
    """`tokenizar("")` no produce tokens y el conteo queda vacío."""
    tokens = tokenizar("")

    assert tokens == []
    assert contar_frecuencias(tokens) == {}


# ---------------------------------------------------------------------------
# 3) Mayúsculas y minúsculas se cuentan como la misma palabra
# ---------------------------------------------------------------------------
def test_mayusculas_y_minusculas_misma_palabra():
    """'Hola', 'hola', 'HOLA', 'HoLa' deben contarse como una sola palabra."""
    texto = "Hola hola HOLA HoLa mundo Mundo MUNDO"

    tokens = tokenizar(texto)
    resultado = contar_frecuencias(tokens)

    # Una única clave "hola" con las 4 apariciones, y "mundo" con 3.
    assert resultado == {"hola": 4, "mundo": 3}
    # Refuerzo explícito: no quedaron variantes con mayúsculas.
    assert "Hola" not in resultado
    assert "HOLA" not in resultado
    assert resultado["hola"] == 4


# ---------------------------------------------------------------------------
# 4) (Extra) Filtrado de stopwords
# ---------------------------------------------------------------------------
def test_sin_stopwords_filtra_palabras_vacias():
    """Con sin_stopwords=True, las stopwords no aparecen en el resultado."""
    # 'el', 'la', 'de', 'que' son stopwords clásicas en español.
    tokens = ["el", "gato", "la", "gato", "de", "casa", "que", "gato"]

    resultado = contar_frecuencias(tokens, sin_stopwords=True)

    assert "el" not in resultado
    assert "la" not in resultado
    assert "de" not in resultado
    assert "que" not in resultado
    assert resultado == {"gato": 3, "casa": 1}


def test_con_stopwords_incluye_palabras_vacias():
    """Con sin_stopwords=False (por defecto), las stopwords sí se cuentan."""
    tokens = ["el", "gato", "el", "gato"]

    resultado = contar_frecuencias(tokens)  # default: sin_stopwords=False

    assert resultado == {"el": 2, "gato": 2}