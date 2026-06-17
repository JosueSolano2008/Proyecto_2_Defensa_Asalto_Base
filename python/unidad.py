class Unidad:
    def __init__(self, nombre, costo, vida, daño, velocidad):
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.daño = daño
        self.velocidad = velocidad
        self.turnos_habilidad = 3
        self.turno_actual = 0
        self.viva = True
        self.congelada = False

    def moverse(self):
        pass

    def atacar(self, objetivo):
        objetivo.vida -= self.daño

    def recibir_daño(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            self.viva = False
class Soldado(Unidad):
    def __init__(self):
        super().__init__(
            nombre="Soldado",
            costo=30,
            vida=60,
            daño=10,
            velocidad=1
        )

    def activar_habilidad(self):
        self.daño *= 2
        print(f"{self.nombre} usó Ataque Doble!")


class Tanque(Unidad):
    def __init__(self):
        super().__init__(
            nombre="Tanque",
            costo=120,
            vida=200,
            daño=25,
            velocidad=1
        )

    def activar_habilidad(self):
        self.escudo = True
        print(f"{self.nombre} activó Escudo Temporal!")

    def recibir_daño(self, cantidad):
        if hasattr(self, 'escudo') and self.escudo:
            self.escudo = False
            print(f"{self.nombre} bloqueó el daño con su escudo!")
        else:
            super().recibir_daño(cantidad)


class UnidadRapida(Unidad):
    def __init__(self):
        super().__init__(
            nombre="Unidad Rápida",
            costo=60,
            vida=40,
            daño=8,
            velocidad=3
        )

    def activar_habilidad(self):
        self.velocidad += 2
        print(f"{self.nombre} aumentó su velocidad!")