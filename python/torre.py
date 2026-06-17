class Torre:
    def __init__(self, nombre, costo, vida, daño, alcance):
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.daño = daño
        self.alcance = alcance
        self.turnos_habilidad = 3
        self.turno_actual = 0
        self.viva = True

    def atacar(self, unidad):
        unidad.vida -= self.daño

    def recibir_daño(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            self.viva = False

    def activar_habilidad(self, unidades):
        # cada subclase define su propia habilidad
        pass

    def actualizar_turno(self, unidades):
        self.turno_actual += 1
        if self.turno_actual >= self.turnos_habilidad:
            self.activar_habilidad(unidades)
            self.turno_actual = 0

    def __str__(self):
        return f"{self.nombre} | Vida: {self.vida} | Daño: {self.daño} | Alcance: {self.alcance}"