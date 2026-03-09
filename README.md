# ⚰️ El Ahorcado

Juego clásico del ahorcado con interfaz gráfica, desarrollado en Python con Tkinter.

## 🚀 Requisitos

- Python 3.x
- Tkinter (incluido por defecto en la mayoría de instalaciones de Python)

## ▶️ Cómo ejecutar

```bash
python ahorcado.py
```

## 🎮 Cómo jugar

1. Al iniciar, se selecciona una palabra al azar y se muestra una pista.
2. Adivina la palabra letra por letra usando el teclado en pantalla o tu teclado físico.
3. Tienes **6 intentos** antes de que el ahorcado esté completo.
4. Si adivinas todas las letras, ¡ganas! Si cometes 6 errores, pierdes.
5. Pulsa **🔄 Nueva Partida** para jugar de nuevo.

## 📦 Estructura del proyecto

```
ahorcado.py   # Archivo principal con toda la lógica y la interfaz
```

## 🗂️ Categorías de palabras

El juego incluye 30 palabras distribuidas en dos temáticas:

- **Tecnología e informática** — python, algoritmo, servidor, software...
- **Mundo cotidiano** — chocolate, mariposa, dinosaurio, aventura...

Cada palabra tiene su propia pista con emoji para facilitar el juego.

## 🎨 Características

- Interfaz oscura con colores personalizados
- Dibujo del ahorcado animado en canvas
- Teclado visual en pantalla + soporte para teclado físico
- Pistas para cada palabra
- Contador de errores e historial de letras incorrectas
- Mensajes de victoria y derrota

## ➕ Añadir palabras

Para agregar palabras propias, edita las listas en `ahorcado.py`:

```python
PALABRAS = [
    ...,
    "tupalabra",
]

PISTAS = {
    ...,
    "tupalabra": "Tu pista aquí 🎯",
}
```

## 📄 Licencia

Proyecto de uso libre. Siéntete libre de modificarlo y distribuirlo.
