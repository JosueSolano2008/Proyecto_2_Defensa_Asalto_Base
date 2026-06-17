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
        pass

    def actualizar_turno(self, unidades):
        self.turno_actual += 1
        if self.turno_actual >= self.turnos_habilidad:
            self.activar_habilidad(unidades)
            self.turno_actual = 0

    def __str__(self):
        return f"{self.nombre} | Vida: {self.vida} | Daño: {self.daño} | Alcance: {self.alcance}"
    
class TorreBasica(Torre):
    def __init__(self):
        super().__init__(
            nombre="Torre Básica",
            costo=50,
            vida=80,
            daño=15,
            alcance=3
        )
        self.turnos_habilidad = 3

    def activar_habilidad(self, unidades):
        objetivos = unidades[:2]
        for unidad in objetivos:
            if unidad.viva:
                unidad.vida -= self.daño
        print(f"{self.nombre} usó Disparo Doble!")


class TorrePesada(Torre):
    def __init__(self):
        super().__init__(
            nombre="Torre Pesada",
            costo=150,
            vida=200,
            daño=40,
            alcance=2
        )
        self.turnos_habilidad = 4

    def activar_habilidad(self, unidades):
        for unidad in unidades:
            if unidad.viva:
                unidad.vida -= self.daño // 2
        print(f"{self.nombre} usó Daño en Área!")


class TorreMagica(Torre):
    def __init__(self):
        super().__init__(
            nombre="Torre Mágica",
            costo=100,
            vida=60,
            daño=10,
            alcance=4
        )
        self.turnos_habilidad = 3

    def activar_habilidad(self, unidades):
        if unidades:
            objetivo = unidades[0]
            if objetivo.viva:
                objetivo.congelada = True
        print(f"{self.nombre} usó Congelar!")