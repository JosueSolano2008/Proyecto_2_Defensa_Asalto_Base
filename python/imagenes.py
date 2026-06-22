# python/imagenes.py
# Carga y cachea las imágenes de torres y unidades por facción.
# Si una imagen no existe o Tkinter no puede cargarla, se devuelve None
# y quien dibuje el mapa debe usar su color de respaldo (fallback).

import os
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

CARPETA_ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Assets")

# Mapa: facción -> tipo de elemento -> nombre de archivo dentro de Assets/<faccion>/
ARCHIVOS = {
    "imperio": {
        "torre_basica": "OscuroBasico.png",
        "torre_pesada": "PesadoOscuro.png",
        "torre_magica": "Magicaoscura.png",
        "unidad_soldado": "BasicoImperio.gif",
        "unidad_rapida": "Medioimperio.gif",
        "unidad_tanque": "FuerteImperio.gif",
    },
    "rebeldes": {
        "torre_basica": "Castillo basico, rebeldes.webp",
        "torre_pesada": "PesadoRebelde.png",
        "torre_magica": "MagicaRebeldes.png",
        "unidad_soldado": "BasicoRebelde.gif",
        "unidad_rapida": "MedioRebelde.gif",
        "unidad_tanque": "FuerteRebelde.gif",
    },
    "reinado": {
        "torre_basica": "torreRegular.png",
        "torre_pesada": "Torre Pesada.png",
        "torre_magica": "TorreMagica.png",
        "unidad_soldado": "BasicoReino.gif",
        "unidad_rapida": "MedioReino.gif",
        "unidad_tanque": "FuerteReino.gif",
    },
}

_CACHE = {}  # (faccion, clave, tamaño) -> PhotoImage

def obtener_imagen(faccion: str, clave: str, tamaño: int = 50, frame_idx: int = 0):
    faccion = (faccion or "").lower()

    if faccion not in ARCHIVOS or clave not in ARCHIVOS[faccion]:
        return None

    cache_key = (faccion, clave, tamaño)

    if cache_key not in _CACHE:
        ruta = os.path.join(CARPETA_ASSETS, faccion.capitalize(), ARCHIVOS[faccion][clave])

        if not os.path.exists(ruta):
            return None

        try:
            img_original = Image.open(ruta)
            frames = []

            for frame in ImageSequence.Iterator(img_original):
                frame = frame.convert("RGBA")
                frame = frame.resize((tamaño, tamaño), Image.LANCZOS)
                frames.append(ImageTk.PhotoImage(frame))

            if not frames:
                return None

            _CACHE[cache_key] = frames

        except Exception as e:
            print(f"Error cargando imagen {ruta}: {e}")
            return None

    frames = _CACHE[cache_key]
    return frames[frame_idx % len(frames)]


def clave_torre(nombre_torre: str) -> str:
    """Traduce el nombre legible de la torre a la clave usada en ARCHIVOS."""
    n = nombre_torre.lower()
    if "pesada" in n:
        return "torre_pesada"
    if "mágica" in n or "magica" in n:
        return "torre_magica"
    return "torre_basica"


def clave_unidad(nombre_unidad: str) -> str:
    """Traduce el nombre legible de la unidad a la clave usada en ARCHIVOS."""
    n = nombre_unidad.lower()
    if "tanque" in n:
        return "unidad_tanque"
    if "rápida" in n or "rapida" in n:
        return "unidad_rapida"
    return "unidad_soldado"
