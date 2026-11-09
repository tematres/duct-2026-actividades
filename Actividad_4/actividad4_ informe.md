## Actividad 4
https://github.com/tematres/duct-2026-actividades

1. ¿Qué pasa si se quita .lower() de analizador.py?
Si se quita el comando que normaliza las cadenas a minúsculas y se proporiconan argumentos como "Sol", "SOL","sol" la prueba de igualdad va a dar falso porque las 3 cadenas no serían iguales. Por esta razón el pytest devolverá "FAILED".

2. ¿Por qué contar_frecuencias recibe un string y no una ruta de archivo?
Es una forma sencilla de despejar problemas, de esta manera de aislan factores y se evalúa sólo la función. Si se utilizara un ruta y un archivo externo, podría haber un error en el archivo o en la ruta, serían 2 aspectos externos a la mecánica de la función.

3. Otro caso de borde y cuarta prueba
Un caso podría ser el caso de un texto con espacios de más o saltos de línea. La 4ta prueba está incorporada en el archivo test_analizador.py  