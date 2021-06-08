El archivo data.py contiene 4 listas, cada una de 100 elementos y una variable.

- La primera lista “mensajes” contiene los 100 mensajes a encriptar.
- La segunda lista “hashes” contiene los hashes de los 100 mensajes (en orden) con el h0 original.
- La tercera lista “keys”, contiene los 100 h0 con los que vamos a probar los mensajes.
- La cuarta lista “keyed_hash” contiene los 100 hashes de los mensajes con sus respectivos h0’s.
- La La variable “original_key” contiene el h0 original.

Los hashes los podemos ver como:  
- `md5(mensajes_i,  original_key) ≡ hashes_i`
- `md5(ensajes_i,  keys_i) ≡ keyed_hash_i`
