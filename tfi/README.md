# analizador.py
Script en Python que analiza la frecuencia de palabras en un archivo de texto y genera un gráfico de barras horizontales con las 10 palabras más frecuentes. Genera los siguientes resultados:
- Imprime en consola el **Top 10** de palabras más frecuentes.
- Guarda un gráfico de barras horizontales en formato PNG con esas 10 palabras (palabras en el eje Y, frecuencia en el eje X).
La lista de stopwords se reutiliza desde `ejercicio_2.py`, por lo que ese archivo debe estar en el mismo directorio que `analizador.py`.
## Cómo usarlo: 
    # Contando todas las palabras (comportamiento original)
    python analizador.py texto.md
    # Filtrando stopwords
    python analizador.py texto.md --sin-stopwords
