"""
analizador.py
Este script hace lo siguiente:
- Recibe como argumento el nombre de un archivo de texto.
- Lee el archivo de texto manejando con try/except el caso de que el archivo no exista o en caso de que el archivo no sea un archivo de texto,
- Cuenta la frecuencia de cada palabra usando un diccionario,
- Si después de filtrar no queda ninguna palabra (p. ej. el archivo solo tiene stopwords), se avisa y se sale con código 1.
- Genere y guarda un gráfico de barras con las 10 palabras más frecuentes usando matplotlib.
- Se guarda como grafico_palabras.png en el directorio actual.
- Cómo usarlo: 
    # Contando todas las palabras (comportamiento original)
    python analizador.py texto.md

    # Filtrando stopwords
    python analizador.py texto.md --sin-stopwords

Requisitos:
- El directorio tiene que tener permisos de escritura para el usuario que ejecuta el script
- El archivo ejercicio_2.py tiene que estar en el mismo directorio que este script, ya que se importa la lista de stopwords desde allí.
- el archivo de texto a analizar tiene que estar en el mismo directorio que este script, o indicar la ruta completa al archivo.
- la librería matplotlib tiene que estar instalada. 
- las librerías argparse y sys son parte de la librería estándar de Python.
"""
import argparse
import sys
import string

try:
    import matplotlib
    matplotlib.use("Agg")  # backend sin pantalla, para guardar a archivo
    import matplotlib.pyplot as plt
except ImportError:
    print("Error: se requiere matplotlib. Instalalo con: pip install matplotlib")
    sys.exit(1)

# Reutilizamos la lista de stopwords definida en ejercicio_2.py
try:
    from ejercicio_2 import STOP_WORDS
except ImportError:
    print("Error: no se pudo importar STOP_WORDS desde 'ejercicio_2.py'. "
          "Asegurate de que el archivo esté en el mismo directorio.")
    sys.exit(1)


def tokenizar(texto):
    """Convierte el texto a minúsculas, quita signos de puntuación y lo separa en palabras."""
    texto = texto.lower()
    for signo in string.punctuation:
        texto = texto.replace(signo, "")
    return texto.split()


def contar_frecuencias(tokens, sin_stopwords=False):
    """
    Cuenta cuántas veces aparece cada palabra usando un diccionario.

    Parametros:
        tokens (list[str]): palabras ya tokenizadas.
        sin_stopwords (bool): si es True, descarta las palabras vacías.
    """
    frecuencias = {}
    for token in tokens:
        if sin_stopwords and token in STOP_WORDS:
            continue
        frecuencias[token] = frecuencias.get(token, 0) + 1
    return frecuencias


def generar_grafico(frecuencias, ruta_salida="grafico_palabras.png", titulo=None):
    """Genera y guarda un gráfico de barras horizontales con las 10 palabras
    más frecuentes (palabras en el eje Y, frecuencia en el eje X)."""
    top10 = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)[:10]
    if not top10:
        print("No hay palabras para graficar.")
        return

    palabras = [p for p, _ in top10]
    valores = [v for _, v in top10]

    # Invertimos el orden para que la palabra más frecuente quede arriba
    palabras = palabras[::-1]
    valores = valores[::-1]

    plt.figure(figsize=(10, 6))
    plt.barh(palabras, valores, color="steelblue")
    plt.title(titulo or "10 palabras más frecuentes")
    plt.xlabel("Frecuencia")
    plt.ylabel("Palabra")
    plt.tight_layout()
    plt.savefig(ruta_salida)
    plt.close()
    print(f"\nGráfico guardado en: {ruta_salida}")


def parsear_argumentos():
    """Define y parsea los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Analiza la frecuencia de palabras en un archivo de texto "
                    "y genera un gráfico de barras con las 10 más frecuentes."
    )
    parser.add_argument(
        "archivo",
        help="Ruta del archivo de texto a analizar."
    )
    parser.add_argument(
        "--sin-stopwords",
        action="store_true",
        help="Si se indica, descarta las palabras vacías (stopwords en español) "
             "antes de contar las frecuencias."
    )
    return parser.parse_args()


def main():
    args = parsear_argumentos()

    # 1) Leer el archivo manejando errores
    try:
        with open(args.archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        print(f"Error: el archivo '{args.archivo}' no existe.")
        sys.exit(1)
    except IsADirectoryError:
        print(f"Error: '{args.archivo}' es un directorio, no un archivo de texto.")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: '{args.archivo}' no parece ser un archivo de texto válido "
              "(posible archivo binario).")
        sys.exit(1)
    except PermissionError:
        print(f"Error: no hay permisos para leer '{args.archivo}'.")
        sys.exit(1)
    except OSError as e:
        print(f"Error al leer el archivo: {e}")
        sys.exit(1)

    # 2) Tokenizar
    tokens = tokenizar(contenido)
    if not tokens:
        print("El archivo no contiene palabras.")
        sys.exit(1)

    # 3) Contar frecuencias (con o sin stopwords según la bandera)
    frecuencias = contar_frecuencias(tokens, sin_stopwords=args.sin_stopwords)
    if not frecuencias:
        print("No quedaron palabras para analizar "
              "(¿el archivo solo contiene stopwords?).")
        sys.exit(1)

    # 4) Mostrar top 10 en consola
    etiqueta = "sin stopwords" if args.sin_stopwords else "todas las palabras"
    print(f"=== Top 10 palabras más frecuentes ({etiqueta}) ===")
    top10 = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)[:10]
    for palabra, freq in top10:
        print(f"  {palabra}: {freq}")

    # 5) Generar gráfico
    sufijo = "sin_stopwords" if args.sin_stopwords else "todas"
    ruta_grafico = f"grafico_palabras_{sufijo}.png"
    titulo = f"10 palabras más frecuentes ({etiqueta})"
    generar_grafico(frecuencias, ruta_salida=ruta_grafico, titulo=titulo)


if __name__ == "__main__":
    main()