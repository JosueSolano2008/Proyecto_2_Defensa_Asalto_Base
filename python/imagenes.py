# python/imagenes.py
# Carga y cachea las imágenes de torres y unidades por facción.
# Si una imagen no existe o Tkinter no puede cargarla, se devuelve None
# y quien dibuje el mapa debe usar su color de respaldo (fallback).

import os
import tkinter as tk
from PIL import Image, ImageTk

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
        "torre_basica": "CastilloBasicoRebelde.png",
        "torre_pesada": "PesadoRebelde.png",
        "torre_magica": "MagicaRebeldes.png",
        "unidad_soldado": "BasicoRebelde.gif",
        "unidad_rapida": "MedioRebelde.gif",
        "unidad_tanque": "FuerteRebelde.gif",
    },
    "reinado": {
        "torre_basica": "torreRegular.png",
        "torre_pesada": "TorrePesada.png",
        "torre_magica": "TorreMagica.png",
        "unidad_soldado": "BasicoReino.gif",
        "unidad_rapida": "MedioReino.gif",
        "unidad_tanque": "FuerteReino.gif",
    },
}

_CACHE = {}  # (faccion, clave, tamaño) -> PhotoImage


def obtener_imagen(faccion: str, clave: str, tamaño: int = 50):
    """Devuelve un ImageTk.PhotoImage ya redimensionado, o None si no existe."""
    faccion = (faccion or "").lower()
    if faccion not in ARCHIVOS or clave not in ARCHIVOS[faccion]:
        return None

    cache_key = (faccion, clave, tamaño)
    if cache_key in _CACHE:
        return _CACHE[cache_key]

    ruta = os.path.join(CARPETA_ASSETS, faccion.capitalize(), ARCHIVOS[faccion][clave])
    if not os.path.exists(ruta):
        return None

    try:
        img = Image.open(ruta).convert("RGBA")
        img = img.resize((tamaño, tamaño), Image.LANCZOS)
        foto = ImageTk.PhotoImage(img)
    except Exception:
        return None

    _CACHE[cache_key] = foto
    return foto


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
