# python/juego.py
from python.torre import Torre, TorreBasica, TorrePesada, TorreMagica, Muro, Base
from python.unidad import Unidad, Soldado, Tanque, UnidadRapida

FILAS = 10
COLUMNAS = 10
FILA_BASE = FILAS // 2
COL_BASE = COLUMNAS // 2
DINERO_INICIAL = 300
DINERO_POR_RONDA = 100
RONDAS_PARA_GANAR = 3
MAX_TURNOS_COMBATE = 50


def crear_mapa():
    mapa = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]
    base = Base()
    mapa[FILA_BASE][COL_BASE] = base
    return mapa, base


def colocar_elemento(mapa, elemento, fila, col):
    if not (0 <= fila < FILAS and 0 <= col < COLUMNAS):
        return False, "Posición fuera del mapa."
    if mapa[fila][col] is not None:
        return False, "La celda ya está ocupada."
    if fila == FILA_BASE and col == COL_BASE:
        return False, "No se puede colocar sobre la base."
    mapa[fila][col] = elemento
    return True, "Colocado correctamente."


def eliminar_elemento(mapa, fila, col):
    mapa[fila][col] = None


def obtener_torres(mapa):
    result = []
    for f in range(FILAS):
        for c in range(COLUMNAS):
            if isinstance(mapa[f][c], Torre) and mapa[f][c].viva:
                result.append((f, c, mapa[f][c]))
    return result


def obtener_unidades(mapa):
    result = []
    for f in range(FILAS):
        for c in range(COLUMNAS):
            if isinstance(mapa[f][c], Unidad) and mapa[f][c].viva:
                result.append((f, c, mapa[f][c]))
    return result


def distancia(f1, c1, f2, c2):
    return abs(f1 - f2) + abs(c1 - c2)


def mover_unidad(mapa, fila, col):
    unidad = mapa[fila][col]
    if not isinstance(unidad, Unidad) or not unidad.viva:
        return fila, col

    f_actual, c_actual = fila, col

    objetivos = [
        (FILA_BASE - 1, COL_BASE),
        (FILA_BASE + 1, COL_BASE),
        (FILA_BASE, COL_BASE - 1),
        (FILA_BASE, COL_BASE + 1),
    ]

    objetivos_validos = []
    for f, c in objetivos:
        if 0 <= f < FILAS and 0 <= c < COLUMNAS:
            objetivos_validos.append((f, c))

    for _ in range(unidad.velocidad):
        mejor_f, mejor_c = f_actual, c_actual

        menor_dist = min(
            abs(f_actual - fo) + abs(c_actual - co)
            for fo, co in objetivos_validos
        )

        for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nf, nc = f_actual + df, c_actual + dc

            if not (0 <= nf < FILAS and 0 <= nc < COLUMNAS):
                continue

            celda = mapa[nf][nc]

            if celda is None:
                nueva_dist = min(
                    abs(nf - fo) + abs(nc - co)
                    for fo, co in objetivos_validos
                )

                if nueva_dist < menor_dist:
                    menor_dist = nueva_dist
                    mejor_f, mejor_c = nf, nc

        if (mejor_f, mejor_c) == (f_actual, c_actual):
            break

        mapa[mejor_f][mejor_c] = mapa[f_actual][c_actual]
        mapa[f_actual][c_actual] = None

        f_actual, c_actual = mejor_f, mejor_c

    return f_actual, c_actual

class Juego:
    def __init__(self, jugador_defensor=None, jugador_atacante=None,
                 faccion_def="imperio", faccion_atk="rebeldes"):
        self.defensor = jugador_defensor
        self.atacante = jugador_atacante
        self.faccion_def = faccion_def
        self.faccion_atk = faccion_atk

        self.rondas_defensor = 0
        self.rondas_atacante = 0
        self.ronda_actual = 1

        self.dinero_defensor = DINERO_INICIAL
        self.dinero_atacante = DINERO_INICIAL

        # Bonus acumulado de daño de la ronda anterior (para el atacante)
        self.bonus_atk_ronda_anterior = 0

        self.mapa, self.base = crear_mapa()
        self.log = []

    def iniciar(self):
        pass

    # ── Compras defensor ──────────────────────────────────────

    def comprar_torre(self, tipo: str, fila: int, col: int):
        fabricas = {
            "basica": lambda: TorreBasica(self.faccion_def),
            "pesada": lambda: TorrePesada(self.faccion_def),
            "magica": lambda: TorreMagica(self.faccion_def),
        }
        if tipo not in fabricas:
            return False, "Tipo de torre inválido."
        torre = fabricas[tipo]()
        if self.dinero_defensor < torre.costo:
            return False, f"Dinero insuficiente. Necesitas ${torre.costo}, tienes ${self.dinero_defensor}."
        ok, msg = colocar_elemento(self.mapa, torre, fila, col)
        if ok:
            self.dinero_defensor -= torre.costo
        return ok, msg

    def comprar_muro(self, fila: int, col: int):
        muro = Muro(self.faccion_def)
        if self.dinero_defensor < muro.costo:
            return False, f"Dinero insuficiente. Necesitas ${muro.costo}."
        ok, msg = colocar_elemento(self.mapa, muro, fila, col)
        if ok:
            self.dinero_defensor -= muro.costo
        return ok, msg

    # ── Compras atacante ──────────────────────────────────────

    def comprar_unidad(self, tipo: str, fila: int, col: int):
        fabricas = {
            "soldado": lambda: Soldado(self.faccion_atk),
            "tanque":  lambda: Tanque(self.faccion_atk),
            "rapida":  lambda: UnidadRapida(self.faccion_atk),
        }
        if tipo not in fabricas:
            return False, "Tipo de unidad inválido."
        unidad = fabricas[tipo]()
        if self.dinero_atacante < unidad.costo:
            return False, f"Dinero insuficiente. Necesitas ${unidad.costo}."
        en_borde = (fila == 0 or fila == FILAS - 1 or col == 0 or col == COLUMNAS - 1)
        if not en_borde:
            return False, "Las unidades deben colocarse en el borde del mapa."
        ok, msg = colocar_elemento(self.mapa, unidad, fila, col)
        if ok:
            self.dinero_atacante -= unidad.costo
        return ok, msg

    # ── Verificar si el atacante puede seguir ────────────────

    def atacante_sin_recursos(self):
        """Retorna True si el atacante no tiene dinero NI unidades en el mapa."""
        tiene_unidades = any(
            isinstance(self.mapa[f][c], Unidad) and self.mapa[f][c].viva
            for f in range(FILAS) for c in range(COLUMNAS)
        )
        return self.dinero_atacante <= 0 and not tiene_unidades

    # ── Combate ───────────────────────────────────────────────

    def ejecutar_combate(self):
        self.log = []
        daño_total_atacante = 0  # acumular para el bonus de siguiente ronda

        # Verificar si el atacante no pudo comprar nada
        if self.atacante_sin_recursos():
            self.log.append("El atacante se quedó sin dinero y sin unidades. Defensor gana.")
            return "defensor"

        for turno in range(1, MAX_TURNOS_COMBATE + 1):
            self.log.append(f"--- Turno {turno} ---")

            # Torres atacan
            for f, c, torre in obtener_torres(self.mapa):
                unidades_en_alcance = [
                    u for fu, cu, u in obtener_unidades(self.mapa)
                    if distancia(f, c, fu, cu) <= torre.alcance
                ]
                torre.actualizar_turno(unidades_en_alcance)
                if unidades_en_alcance:
                    objetivo = unidades_en_alcance[0]
                    torre.atacar(objetivo)
                    self.log.append(f"  {torre.nombre} → {objetivo.nombre} ({objetivo.vida} HP)")
                    if objetivo.vida <= 0:
                        objetivo.viva = False
                        recompensa = objetivo.costo // 2
                        self.dinero_defensor += recompensa
                        self.log.append(f"  ✓ {objetivo.nombre} eliminado. Defensor +${recompensa}")

            # Limpiar muertos
            for f in range(FILAS):
                for c in range(COLUMNAS):
                    if isinstance(self.mapa[f][c], Unidad) and not self.mapa[f][c].viva:
                        self.mapa[f][c] = None

            # Unidades se mueven y atacan
            for f, c, unidad in list(obtener_unidades(self.mapa)):
                if not unidad.viva:
                    continue
                if unidad.congelada:
                    unidad.congelada = False
                    self.log.append(f"  {unidad.nombre} congelada, pierde turno.")
                    continue

                nf, nc = mover_unidad(self.mapa, f, c)

                if nf == FILA_BASE and nc == COL_BASE:
                    self.base.recibir_daño(unidad.daño)
                    daño_total_atacante += unidad.daño
                    self.dinero_atacante += unidad.daño
                    self.log.append(f"  {unidad.nombre} atacó la BASE. HP: {self.base.vida}")
                    if not self.base.viva:
                        self.log.append("  ¡BASE DESTRUIDA! Atacante gana.")
                        self.bonus_atk_ronda_anterior = daño_total_atacante
                        return "atacante"
                else:
                    for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        af, ac = nf + df, nc + dc
                        if not (0 <= af < FILAS and 0 <= ac < COLUMNAS):
                            continue
                        obj = self.mapa[af][ac]
                        if isinstance(obj, (Torre, Muro)) and obj.viva:
                            obj.recibir_daño(unidad.daño)
                            daño_total_atacante += unidad.daño
                            self.dinero_atacante += unidad.daño // 2
                            self.log.append(f"  {unidad.nombre} atacó {obj.nombre} ({obj.vida} HP)")
                            if not obj.viva:
                                self.mapa[af][ac] = None
                                bonus = obj.costo // 3
                                self.dinero_atacante += bonus
                                self.log.append(f"  ✓ {obj.nombre} destruido. Atacante +${bonus}")
                            break

                unidad.actualizar_turno()

            if not obtener_unidades(self.mapa):
                self.log.append("  Todas las unidades eliminadas. Defensor gana.")
                self.bonus_atk_ronda_anterior = daño_total_atacante
                return "defensor"

        self.log.append("Tiempo agotado. Defensor gana.")
        self.bonus_atk_ronda_anterior = daño_total_atacante
        return "defensor"

    # ── Control de rondas ─────────────────────────────────────

    def registrar_victoria_ronda(self, ganador: str):
        if ganador == "defensor":
            self.rondas_defensor += 1
        else:
            self.rondas_atacante += 1

    def hay_ganador_partida(self):
        if self.rondas_defensor >= RONDAS_PARA_GANAR:
            return self.defensor, "defensor"
        if self.rondas_atacante >= RONDAS_PARA_GANAR:
            return self.atacante, "atacante"
        return None, None

    def iniciar_nueva_ronda(self):
        self.ronda_actual += 1
        self.mapa, self.base = crear_mapa()
        self.dinero_defensor += DINERO_POR_RONDA
        # El atacante recibe dinero base + bonus por daño de ronda anterior
        self.dinero_atacante += DINERO_POR_RONDA + self.bonus_atk_ronda_anterior
        if self.bonus_atk_ronda_anterior > 0:
            self.log = [f"[Bonus atacante por daño previo: +${self.bonus_atk_ronda_anterior}]"]
        else:
            self.log = []
        self.bonus_atk_ronda_anterior = 0

    def estado_marcador(self):
        return {
            "ronda": self.ronda_actual,
            "rondas_defensor": self.rondas_defensor,
            "rondas_atacante": self.rondas_atacante,
            "dinero_defensor": self.dinero_defensor,
            "dinero_atacante": self.dinero_atacante,
            "vida_base": self.base.vida,
        }
