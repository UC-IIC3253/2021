# Solución pregunta 3 Tarea 1

Aunque la solución de esta tarea debía ser un Jupyter notebook, esta solución se entrega en el archivo `solucion.py` para que sea más fácil de probar. Para entender la solución se puede mirar dicho archivo, sus funciones y razonamiento contienen la documentación necesaria.

## Dependencias

El archivo `solucion.py` utiliza la función `xor` definida en `otp_utils.py`, y tiene las dependencias especificadas en el archivo `Pipfile`. Estas dependencias se pueden instalar a mano usando [pip](https://pypi.org/project/pip/), o de forma más directa utilizando [pipenv](https://pipenv.pypa.io/en/latest/)

## Ejecución

Una vez instaladas las dependencias, se puede probar la solución utilizando su correo y número de alumno, simplemente llamando a
```python
python solucion.py <email_uc> <n_alumno>
```
Esto supone que ha clonado correctamente el repositorio del curso y por tanto la planilla con los mensajes encriptados se encuentra en `../../mensajes_pregunta_3/mensajes_p3.csv`.
