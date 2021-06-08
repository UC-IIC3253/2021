# Custom test utilizado en corrección

En el mismo espíritu que el archivo `mensajes_pregunta_3.csv` entregado mientras confeccionaban sus tareas, creamos el archivo `mensajes_pregunta_3_custom.csv`. Este es tal que la primera columna corresponde a una llave `k` en binario y la segunda columna corresponde al mensaje encriptado mediante OTP `Enc(m,k)` en binario.

Los mensajes corresponden a los primeros 2000 caracteres del [guión de la película Pixels (2015)](https://pastebin.com/jKgsVYaU), separados en pedazos de 10 caracteres cada uno (en total 200 mensajes).

Al igual que en `mensajes_pregunta_3.csv`, se asegura que cada llave `k` utilizada para encriptar los mensajes se repite al menos 15 veces.

Para la corrección utilizamos solo la segunda columna como input para la función `break_random_otp` que debian entregar. Y luego comprobando cuántos ataques exitosos se consiguen (leer rúbrica).
