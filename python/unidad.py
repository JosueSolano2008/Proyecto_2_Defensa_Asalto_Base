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