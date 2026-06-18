# python/jugador.py
# Sistema de registro, login y ranking: trabajo conjunto de ambos integrantes.
import json
import os

archivo_jugadores = "jugadores.json"


class Jugador:
    def __init__(self, nombre_usuario: str, contrasenia: str, victorias_defensor=0, victorias_atacante=0):
        self.nombre_usuario = nombre_usuario
        self.contrasenia = contrasenia
        self.victorias_defensor = victorias_defensor
        self.victorias_atacante = victorias_atacante

    def cargar_jugadores(self):
        if not os.path.exists(archivo_jugadores):
            return {"jugadores": {}}
        with open(archivo_jugadores, "r") as f:
            return json.load(f)

    def guardar_jugadores(self, datos):
        with open(archivo_jugadores, "w") as f:
            json.dump(datos, f, indent=4)

    def registrar(self):
        datos = self.cargar_jugadores()
        if self.nombre_usuario in datos["jugadores"]:   # ← minúscula corregida
            return False, "El usuario ya existe."
        datos["jugadores"][self.nombre_usuario] = {     # ← minúscula corregida
            "contrasena": self.contrasenia,             # ← sin ñ (consistente)
            "victorias_defensor": self.victorias_defensor,
            "victorias_atacante": self.victorias_atacante,
        }
        self.guardar_jugadores(datos)
        return True, "Usuario registrado correctamente."

    def iniciar_sesion(self, nombre_usuario, contrasenia):
        datos = self.cargar_jugadores()
        if nombre_usuario not in datos["jugadores"]:
            return None, "El usuario no existe."
        info = datos["jugadores"][nombre_usuario]
        if info["contrasena"] != contrasenia:
            return None, "Contraseña incorrecta."
        jugador = Jugador(
            nombre_usuario,
            contrasenia,
            info["victorias_defensor"],
            info["victorias_atacante"],
        )
        return jugador, "Sesión iniciada correctamente."

    def agregar_victoria(self, rol):
        if rol == "defensor":
            self.victorias_defensor += 1
        elif rol == "atacante":
            self.victorias_atacante += 1
        datos = self.cargar_jugadores()
        datos["jugadores"][self.nombre_usuario] = {
            "contrasena": self.contrasenia,
            "victorias_defensor": self.victorias_defensor,
            "victorias_atacante": self.victorias_atacante,
        }
        self.guardar_jugadores(datos)

    def obtener_top(self, rol, cantidad=5):
        datos = self.cargar_jugadores()
        ranking = [
            {"nombre": nombre, "victorias": info[f"victorias_{rol}"]}
            for nombre, info in datos["jugadores"].items()
        ]
        ranking.sort(key=lambda x: x["victorias"], reverse=True)
        return ranking[:cantidad]
