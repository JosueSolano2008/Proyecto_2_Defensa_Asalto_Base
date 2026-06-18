# python/unidad.py
# Diseño de clases, valores y habilidades: trabajo conjunto de ambos integrantes.

class Unidad:
    def __init__(self, nombre, costo, vida, daño, velocidad, faccion="imperio"):
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.daño = daño
        self.velocidad = velocidad
        self.faccion = faccion
        self.turnos_habilidad = 3
        self.turno_actual = 0
        self.viva = True
        self.congelada = False

    def atacar(self, objetivo):
        objetivo.vida -= self.daño

    def recibir_daño(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            self.viva = False

    def activar_habilidad(self):
        pass

    def actualizar_turno(self):
        self.turno_actual += 1
        if self.turno_actual >= self.turnos_habilidad:
            self.activar_habilidad()
            self.turno_actual = 0

    def __str__(self):
        return f"{self.nombre} | Vida: {self.vida} | Daño: {self.daño} | Velocidad: {self.velocidad}"


class Soldado(Unidad):
    def __init__(self, faccion="imperio"):
        super().__init__("Soldado", costo=30, vida=60, daño=10, velocidad=1, faccion=faccion)

    def activar_habilidad(self):
        self.daño *= 2
        print(f"{self.nombre} usó Ataque Doble!")


class Tanque(Unidad):
    def __init__(self, faccion="imperio"):
        super().__init__("Tanque", costo=120, vida=200, daño=25, velocidad=1, faccion=faccion)
        self.escudo = False

    def activar_habilidad(self):
        self.escudo = True
        print(f"{self.nombre} activó Escudo Temporal!")

    def recibir_daño(self, cantidad):
        if self.escudo:
            self.escudo = False
            print(f"{self.nombre} bloqueó el daño con su escudo!")
        else:
            super().recibir_daño(cantidad)


class UnidadRapida(Unidad):
    def __init__(self, faccion="imperio"):
        super().__init__("Unidad Rápida", costo=60, vida=40, daño=8, velocidad=3, faccion=faccion)

    def activar_habilidad(self):
        self.velocidad += 2
        print(f"{self.nombre} aumentó su velocidad!")
