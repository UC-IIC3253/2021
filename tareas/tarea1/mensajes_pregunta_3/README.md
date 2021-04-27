# Instrucciones para escuchar el canal entre Alice y Bob

En este directorio se encuentra el archivo `mensajes_pregunta_3.csv`, que contiene los mensajes encriptados que le ha enviado Alice a Bob. Cada fila de este archivo contiene dos elementos, que llamaremos el *índice* y el *texto cifrado*.

## Índice
**Importante:** Para todas las construcciones que vienen a continuación, se considera que si un número de alumno tiene algún caracter no numérico, dicho caracter se remplaza por un cero. Usaremos la extensión `@uc.cl` para todos los correos de la universidad.

Supondremos que Alice y Bob han decidido hablar por varios canales distintos, donde cada canal puede ser escuchado por un estudiante del curso. El índice de cada mensaje determinará qué canal se está usando. Aunque no sabemos a priori cuántas veces se ha utilizado cada canal, sí conocemos cómo se construyen los índices para cada canal:

Si una persona tiene número de alumno `<numero_alumno>` y correo `<email_uc>`, el índice del i-ésimo mensaje enviado por el canal correspondiente a esa persona se define como `md5(<email_uc>, <numero_alumno> * 100 + i)`, donde `md5` es la función que se le ha pedido programar en la Pregunta 2 de esta tarea.

## Texto cifrado
El texto cifrado de cada fila se construye de acuerdo a lo especificado en el enunciado: es la codificación binaria del resultado de encriptar, usando OTP, un mensaje en inglés con alguna de las llaves que comparten Alice y Bob. Es importante mencionar que cada caracter es codificado en un byte (8 bits) y que el XOR se aplica bit a bit. Por ejemplo, si el primer caracter de la llave es `@` (64 en ASCII, 01000000 en binario) y el primer caracter del mensaje es `a` (97 en ASCII, 01100001 en binario), entonces el primer caracter del texto cifrado será `!` (33 en ASCII, 00100001 en binario).

## Sobre la evaluación
Parte de la evaluación de esta pregunta se hará con los mismos mensajes cifrados que se encuentran en el archivo `mensajes_pregunta_3.csv`, pero también se probará con otros mensajes y otras llaves.

---

#### Desafíos!

- De dónde se obtuvieron estos mensajes?
- Podremos escuchar los canales de otras personas **sin** pedirles su correo ni número de alumno?

