# Custom test utilizado en corrección

En esta carpeta se encuentran los mensajes utilizados en la corrección de la Pregunta 2 de la Tarea 3.

La corrección consistió en lo siguiente. Sea  `m_i` el i-ésimo mensaje utilizado para corregir:
1. Llamar a `generar_clave_ElGamal()`.
2. Para cada `m_i`, generar `e_i, s_i = firmar_Schnorr(m_i)`
3. El i-ésimo test consiste en verificar que: (1) `verificar_firma_Schnorr(m_i, (e_i, s_i) == True` y (2) `verificar_firma_Schnorr(m_i, (e_j, s_j) == False` para todo `i != j`.

En total son 12 tests, y cada test corresponde a 0.5 puntos para la pregunta.

Una nota menor es que los pares `(mensaje_1.txt`, `mensaje_2.txt)` y `(mensaje_6.txt`, `mensaje_7.txt)` son tales que difieren en solo una letra (por lo que sus firmas debiesen resultar distintas).