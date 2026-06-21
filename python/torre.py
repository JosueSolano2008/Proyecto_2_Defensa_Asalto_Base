# python/torre.py
# Diseño de clases, valores y habilidades: trabajo conjunto de ambos integrantes.

class Torre:
    def __init__(self, nombre, costo, vida, daño, alcance, faccion="imperio"):
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.daño = daño
        self.alcance = alcance
        self.faccion = faccion
        self.turnos_habilidad = 3
        self.turno_actual = 0
        self.viva = True

    def atacar(self, unidad):
        unidad.recibir_daño(self.daño)

    def recibir_daño(self, cantidad):
        self.vida -= cantidad

        if self.vida <= 0:
            self.vida = 0
            self.viva = False

    def activar_habilidad(self, unidades):
        pass

    def actualizar_turno(self, unidades):
        self.turno_actual += 1
        if self.turno_actual >= self.turnos_habilidad:
            self.activar_habilidad(unidades)
            self.turno_actual = 0

    def __str__(self):
        return f"{self.nombre} | Vida: {self.vida} | Daño: {self.daño} | Alcance: {self.alcance}"


class TorreBasica(Torre):
    def __init__(self, faccion="imperio"):
        super().__init__("Torre Básica", costo=50, vida=80, daño=15, alcance=3, faccion=faccion)
        self.turnos_habilidad = 3

    def activar_habilidad(self, unidades):
        # Disparo Doble: ataca a las dos primeras unidades en alcance
        objetivos = [u for u in unidades if u.viva][:2]
        for unidad in objetivos:
            unidad.recibir_daño(self.daño)
        print(f"{self.nombre} usó Disparo Doble!")


class TorrePesada(Torre):
    def __init__(self, faccion="imperio"):
        super().__init__("Torre Pesada", costo=150, vida=200, daño=40, alcance=2, faccion=faccion)
        self.turnos_habilidad = 4

    def activar_habilidad(self, unidades):
        for unidad in unidades:
            if unidad.viva:
                unidad.vida -= self.daño // 2
        print(f"{self.nombre} usó Daño en Área!")


class TorreMagica(Torre):
    def __init__(self, faccion="imperio"):
        super().__init__("Torre Mágica", costo=100, vida=60, daño=10, alcance=4, faccion=faccion)
        self.turnos_habilidad = 3

    def activar_habilidad(self, unidades):
        if unidades:
            objetivo = unidades[0]
            if objetivo.viva:
                objetivo.congelada = True
        print(f"{self.nombre} usó Congelar!")


class Muro:
    def __init__(self, faccion="imperio"):
        self.nombre = "Muro"
        self.costo = 20
        self.vida = 150
        self.viva = True
        self.faccion = faccion

    def recibir_daño(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            self.vida = 0
            self.viva = False

    def __str__(self):
        return f"Muro | Vida: {self.vida}"


class Base:
    def __init__(self):
        self.nombre = "Base Central"
        self.vida = 500
        self.viva = True

    def recibir_daño(self, cantidad):
        self.vida -= cantidad

        if self.vida <= 0:
            self.vida = 0
            self.viva = False

    def __str__(self):
        return f"Base Central | Vida: {self.vida}"
