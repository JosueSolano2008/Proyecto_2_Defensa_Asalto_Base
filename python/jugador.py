import json
import os

archivo_jugadores = "jugadores.json"

class Jugador:
    def __init__(self, nombre_usuario:str, contrasenia: str):
        self.nombre_usuario = nombre_usuario
        self.contrasenia = contrasenia
        self.victorias_defensor = 0
        self.victorias_atacante = 0
