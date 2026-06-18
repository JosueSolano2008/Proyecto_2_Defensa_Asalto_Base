# main.py - Punto de entrada del juego
import tkinter as tk
from tkinter import messagebox
from python.jugador import Jugador
from python.juego import Juego, FILAS, COLUMNAS, FILA_BASE, COL_BASE
from python.torre import Torre, TorreBasica, TorrePesada, TorreMagica, Muro, Base
from python.unidad import Unidad
from python.imagenes import obtener_imagen, clave_torre, clave_unidad

FACCIONES = ["imperio", "rebeldes", "reinado"]

COLORES = {
    "bg":      "#1a1a2e",
    "panel":   "#16213e",
    "acento":  "#0f3460",
    "boton":   "#e94560",
    "boton2":  "#0f3460",
    "texto":   "#eaeaea",
    "subtexto":"#a0a0b0",
    "entrada": "#0d1b2a",
    "borde":   "#e94560",
}

FACCIONES_COLORES = {
    "imperio":  "#8B4513",
    "rebeldes": "#228B22",
    "reinado":  "#4682B4",
}

CELDA_COLORES = {
    "vacia":    "#2d5a27",
    "base":     "#FFD700",
    "muro":     "#808080",
    "torre":    {"imperio": "#8B4513", "rebeldes": "#228B22", "reinado": "#4682B4"},
    "unidad":   {"imperio": "#cc3300", "rebeldes": "#ff6600", "reinado": "#884400"},
}

TAMAÑO_CELDA = 58

# ── Helpers UI ────────────────────────────────────────────────

def mk_entry(parent, var, ancho=22, ocultar=False):
    e = tk.Entry(parent, textvariable=var, width=ancho,
                 bg=COLORES["entrada"], fg=COLORES["texto"],
                 insertbackground=COLORES["texto"], relief="flat",
                 font=("Consolas", 11), highlightthickness=1,
                 highlightbackground=COLORES["borde"],
                 highlightcolor=COLORES["acento"],
                 show="*" if ocultar else "")
    return e

def mk_btn(parent, texto, cmd, color=None, ancho=16):
    return tk.Button(parent, text=texto, command=cmd, width=ancho,
                     bg=color or COLORES["boton"], fg="white",
                     activebackground=COLORES["acento"], activeforeground="white",
                     relief="flat", font=("Consolas", 10, "bold"), cursor="hand2")

def mk_label(parent, texto, size=11, bold=False, color=None, bg=None):
    return tk.Label(parent, text=texto,
                    bg=bg or COLORES["panel"], fg=color or COLORES["texto"],
                    font=("Consolas", size, "bold" if bold else "normal"))

def mk_titulo(parent, texto, size=14):
    return tk.Label(parent, text=texto, bg=COLORES["bg"],
                    fg=COLORES["boton"], font=("Consolas", size, "bold"))

def centrar(root, w, h):
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")


# ── Pantalla Login ─────────────────────────────────────────────

class PantallaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Defensa y Asalto de Base")
        self.root.configure(bg=COLORES["bg"])
        self.root.resizable(False, False)
        centrar(root, 520, 570)

        self.jugadores_auth = [None, None]
        self.frame = tk.Frame(root, bg=COLORES["bg"])
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        mk_titulo(self.frame, "⚔  DEFENSA Y ASALTO DE BASE  ⚔", 13).pack(pady=(10, 18))

        self.vars = []
        self._labels_estado = []
        roles = ["Jugador 1  (Defensor)", "Jugador 2  (Atacante)"]

        for i in range(2):
            panel = tk.Frame(self.frame, bg=COLORES["panel"],
                             highlightthickness=1, highlightbackground=COLORES["borde"])
            panel.pack(fill="x", padx=10, pady=8, ipady=8)

            mk_label(panel, roles[i], size=12, bold=True,
                     color=COLORES["boton"]).grid(row=0, column=0, columnspan=2, pady=(8, 4))

            mk_label(panel, "Usuario:").grid(row=1, column=0, sticky="e", padx=8, pady=3)
            mk_label(panel, "Contraseña:").grid(row=2, column=0, sticky="e", padx=8, pady=3)

            vu, vp = tk.StringVar(), tk.StringVar()
            self.vars.append((vu, vp))
            mk_entry(panel, vu).grid(row=1, column=1, padx=8, pady=3)
            mk_entry(panel, vp, ocultar=True).grid(row=2, column=1, padx=8, pady=3)

            bf = tk.Frame(panel, bg=COLORES["panel"])
            bf.grid(row=3, column=0, columnspan=2, pady=(6, 2))
            mk_btn(bf, "Registrar", lambda j=i: self._registrar(j),
                   color=COLORES["boton2"], ancho=12).pack(side="left", padx=5)
            mk_btn(bf, "Iniciar sesión", lambda j=i: self._login(j),
                   ancho=12).pack(side="left", padx=5)

            lbl = tk.Label(panel, text="", bg=COLORES["panel"],
                           fg="#00cc66", font=("Consolas", 9))
            lbl.grid(row=4, column=0, columnspan=2, pady=(2, 4))
            self._labels_estado.append(lbl)

        mk_btn(self.frame, "▶  Continuar", self._continuar, ancho=22).pack(pady=(14, 4))
        tk.Label(self.frame,
                 text="Ambos jugadores deben autenticarse antes de continuar.",
                 bg=COLORES["bg"], fg=COLORES["subtexto"],
                 font=("Consolas", 8)).pack()

    def _registrar(self, idx):
        u, p = self.vars[idx][0].get().strip(), self.vars[idx][1].get().strip()
        if not u or not p:
            messagebox.showwarning("Campos vacíos", "Ingresa usuario y contraseña.")
            return
        ok, msg = Jugador(u, p).registrar()
        color = "#00cc66" if ok else "#e94560"
        self._labels_estado[idx].config(text=f"{'✓' if ok else '✗'} {msg}", fg=color)

    def _login(self, idx):
        u, p = self.vars[idx][0].get().strip(), self.vars[idx][1].get().strip()
        if not u or not p:
            messagebox.showwarning("Campos vacíos", "Ingresa usuario y contraseña.")
            return
        jugador, msg = Jugador(u, p).iniciar_sesion(u, p)
        if jugador:
            self.jugadores_auth[idx] = jugador
            self._labels_estado[idx].config(text=f"✓ Sesión: {u}", fg="#00cc66")
        else:
            self._labels_estado[idx].config(text=f"✗ {msg}", fg="#e94560")

    def _continuar(self):
        if None in self.jugadores_auth:
            messagebox.showwarning("Faltan jugadores", "Ambos deben iniciar sesión.")
            return
        if self.jugadores_auth[0].nombre_usuario == self.jugadores_auth[1].nombre_usuario:
            messagebox.showwarning("Error", "Los jugadores no pueden ser el mismo usuario.")
            return
        self.frame.destroy()
        PantallaFaccion(self.root, self.jugadores_auth[0], self.jugadores_auth[1])


# ── Pantalla Facción ───────────────────────────────────────────

class PantallaFaccion:
    def __init__(self, root, j1, j2):
        self.root = root
        self.j1, self.j2 = j1, j2
        self.sel = [tk.StringVar(value=""), tk.StringVar(value="")]

        self.frame = tk.Frame(root, bg=COLORES["bg"])
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        mk_titulo(self.frame, "⚑  ELIGE TU FACCIÓN  ⚑", 14).pack(pady=(10, 4))
        tk.Label(self.frame,
                 text="El defensor y el atacante no pueden usar la misma facción.",
                 bg=COLORES["bg"], fg=COLORES["subtexto"],
                 font=("Consolas", 9)).pack(pady=(0, 16))

        nombres = [f"Jugador 1 — {j1.nombre_usuario}  (Defensor)",
                   f"Jugador 2 — {j2.nombre_usuario}  (Atacante)"]

        for i in range(2):
            panel = tk.Frame(self.frame, bg=COLORES["panel"],
                             highlightthickness=1, highlightbackground=COLORES["borde"])
            panel.pack(fill="x", padx=10, pady=8, ipady=10)
            mk_label(panel, nombres[i], size=11, bold=True,
                     color=COLORES["boton"]).pack(pady=(8, 6))

            row = tk.Frame(panel, bg=COLORES["panel"])
            row.pack()
            for fac in FACCIONES:
                color_fac = FACCIONES_COLORES[fac]
                tk.Radiobutton(
                    row, text=fac.capitalize(), variable=self.sel[i], value=fac,
                    bg=COLORES["panel"], fg=COLORES["texto"],
                    selectcolor=color_fac, activebackground=COLORES["panel"],
                    activeforeground=COLORES["texto"],
                    font=("Consolas", 11, "bold"), indicatoron=False,
                    width=12, relief="flat", cursor="hand2"
                ).pack(side="left", padx=6)

        mk_btn(self.frame, "▶  Confirmar y jugar", self._confirmar, ancho=22).pack(pady=(18, 4))

    def _confirmar(self):
        f1, f2 = self.sel[0].get(), self.sel[1].get()
        if not f1 or not f2:
            messagebox.showwarning("Selección incompleta", "Ambos deben elegir una facción.")
            return
        if f1 == f2:
            messagebox.showwarning("Facción repetida", "No pueden elegir la misma facción.")
            return
        juego = Juego(self.j1, self.j2, faccion_def=f1, faccion_atk=f2)
        self.frame.destroy()
        centrar(self.root, COLUMNAS * TAMAÑO_CELDA + 260, FILAS * TAMAÑO_CELDA + 60)
        PantallaMapa(self.root, juego)


# ── Pantalla Mapa ──────────────────────────────────────────────

FASE_DEF = "FASE_DEFENSOR"
FASE_ATK = "FASE_ATACANTE"
FASE_COM = "COMBATE"

class PantallaMapa:
    def __init__(self, root, juego):
        self.root = root
        self.juego = juego
        self.fase = FASE_DEF
        self.seleccion = tk.StringVar(value="basica")

        self.frame = tk.Frame(root, bg=COLORES["bg"])
        self.frame.pack(fill="both", expand=True)

        self._construir_ui()
        self.dibujar_mapa()

    def _construir_ui(self):
        # Canvas del mapa
        canvas_frame = tk.Frame(self.frame, bg=COLORES["bg"])
        canvas_frame.pack(side="left", padx=10, pady=10)

        self.canvas = tk.Canvas(canvas_frame,
                                width=COLUMNAS * TAMAÑO_CELDA,
                                height=FILAS * TAMAÑO_CELDA,
                                bg="#2d5a27", highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._click_celda)

        # Panel lateral
        panel = tk.Frame(self.frame, bg=COLORES["panel"], width=240)
        panel.pack(side="left", fill="y", padx=(0, 10), pady=10)
        panel.pack_propagate(False)

        # Marcador
        self.lbl_fase = mk_label(panel, "", size=11, bold=True,
                                  color=COLORES["boton"], bg=COLORES["panel"])
        self.lbl_fase.pack(pady=(14, 2))

        self.lbl_ronda = mk_label(panel, "", size=10, bg=COLORES["panel"])
        self.lbl_ronda.pack()
        self.lbl_dinero = mk_label(panel, "", size=10, bg=COLORES["panel"])
        self.lbl_dinero.pack()
        self.lbl_base = mk_label(panel, "", size=10, bg=COLORES["panel"])
        self.lbl_base.pack(pady=(0, 10))

        sep = tk.Frame(panel, bg=COLORES["borde"], height=1)
        sep.pack(fill="x", padx=10, pady=4)

        # Sección defensor
        self.frame_def = tk.Frame(panel, bg=COLORES["panel"])
        self.frame_def.pack(fill="x", padx=8)
        mk_label(self.frame_def, "── TORRES ──", size=9,
                 color=COLORES["subtexto"], bg=COLORES["panel"]).pack(pady=(4, 2))

        opciones_def = [
            ("Torre Básica  $50",  "basica"),
            ("Torre Pesada  $150", "pesada"),
            ("Torre Mágica  $100", "magica"),
            ("Muro          $20",  "muro"),
        ]
        for texto, val in opciones_def:
            tk.Radiobutton(
                self.frame_def, text=texto, variable=self.seleccion, value=val,
                bg=COLORES["panel"], fg=COLORES["texto"], selectcolor=COLORES["acento"],
                activebackground=COLORES["panel"], font=("Consolas", 9),
                indicatoron=True, anchor="w"
            ).pack(fill="x", padx=4)

        # Sección atacante
        self.frame_atk = tk.Frame(panel, bg=COLORES["panel"])
        mk_label(self.frame_atk, "── UNIDADES ──", size=9,
                 color=COLORES["subtexto"], bg=COLORES["panel"]).pack(pady=(4, 2))

        opciones_atk = [
            ("Soldado       $30",  "soldado"),
            ("Tanque        $120", "tanque"),
            ("Unidad Rápida $60",  "rapida"),
        ]
        for texto, val in opciones_atk:
            tk.Radiobutton(
                self.frame_atk, text=texto, variable=self.seleccion, value=val,
                bg=COLORES["panel"], fg=COLORES["texto"], selectcolor=COLORES["acento"],
                activebackground=COLORES["panel"], font=("Consolas", 9),
                indicatoron=True, anchor="w"
            ).pack(fill="x", padx=4)

        sep2 = tk.Frame(panel, bg=COLORES["borde"], height=1)
        sep2.pack(fill="x", padx=10, pady=6)

        self.lbl_msg = tk.Label(panel, text="", bg=COLORES["panel"],
                                fg="#ffcc00", font=("Consolas", 8),
                                wraplength=220, justify="left")
        self.lbl_msg.pack(padx=6, pady=2)

        self.btn_terminar = mk_btn(panel, "▶ Terminar fase", self._terminar_fase, ancho=20)
        self.btn_terminar.pack(pady=(8, 4))

        mk_btn(panel, "Ver Ranking", self._ver_ranking,
               color=COLORES["boton2"], ancho=20).pack(pady=2)

        self._actualizar_panel()

    def _actualizar_panel(self):
        marcador = self.juego.estado_marcador()
        if self.fase == FASE_DEF:
            self.lbl_fase.config(text=f"FASE: DEFENSOR")
            self.lbl_dinero.config(
                text=f"Dinero: ${marcador['dinero_defensor']}")
            self.frame_def.pack(fill="x", padx=8)
            self.frame_atk.pack_forget()
            self.seleccion.set("basica")
        elif self.fase == FASE_ATK:
            self.lbl_fase.config(text="FASE: ATACANTE")
            self.lbl_dinero.config(
                text=f"Dinero: ${marcador['dinero_atacante']}")
            self.frame_def.pack_forget()
            self.frame_atk.pack(fill="x", padx=8)
            self.seleccion.set("soldado")
        else:
            self.lbl_fase.config(text="⚔ COMBATE ⚔")

        self.lbl_ronda.config(
            text=f"Ronda {marcador['ronda']}  |  "
                 f"DEF {marcador['rondas_defensor']} - {marcador['rondas_atacante']} ATK")
        self.lbl_base.config(text=f"Base HP: {marcador['vida_base']}")

    def dibujar_mapa(self):
        self.canvas.delete("all")
        mapa = self.juego.mapa
        self._refs_img = []  # evita que Tkinter libere las imágenes (garbage collector)

        for fila in range(FILAS):
            for col in range(COLUMNAS):
                x1 = col * TAMAÑO_CELDA
                y1 = fila * TAMAÑO_CELDA
                x2 = x1 + TAMAÑO_CELDA
                y2 = y1 + TAMAÑO_CELDA
                cx, cy = x1 + TAMAÑO_CELDA // 2, y1 + TAMAÑO_CELDA // 2

                celda = mapa[fila][col]
                imagen = None

                if celda is None:
                    color = CELDA_COLORES["vacia"]
                    texto = ""
                elif isinstance(celda, Base):
                    color = CELDA_COLORES["base"]
                    texto = "BASE"
                elif isinstance(celda, Muro):
                    fac = getattr(celda, "faccion", "imperio")
                    color = FACCIONES_COLORES.get(fac, "#808080")
                    texto = "M"
                elif isinstance(celda, Torre):
                    fac = getattr(celda, "faccion", "imperio")
                    color = FACCIONES_COLORES.get(fac, "#1E90FF")
                    tipo = celda.nombre[6] if len(celda.nombre) > 6 else "T"
                    texto = f"T{tipo}\n{celda.vida}HP"
                    imagen = obtener_imagen(fac, clave_torre(celda.nombre), TAMAÑO_CELDA)
                elif isinstance(celda, Unidad):
                    fac = getattr(celda, "faccion", "imperio")
                    color = CELDA_COLORES["unidad"].get(fac, "#FF4500")
                    texto = f"{celda.nombre[:3]}\n{celda.vida}HP"
                    imagen = obtener_imagen(fac, clave_unidad(celda.nombre), TAMAÑO_CELDA)
                else:
                    color = CELDA_COLORES["vacia"]
                    texto = ""

                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color, outline="#1a1a2e", width=1)
                if imagen is not None:
                    self._refs_img.append(imagen)
                    self.canvas.create_image(cx, cy, image=imagen)
                    if texto:
                        self.canvas.create_text(cx, y2 - 6, text=texto.split("\n")[-1],
                                                fill="white", font=("Consolas", 7, "bold"))
                elif texto:
                    self.canvas.create_text(cx, cy, text=texto,
                                            fill="white", font=("Consolas", 7, "bold"),
                                            justify="center")

    def _click_celda(self, event):
        col = event.x // TAMAÑO_CELDA
        fila = event.y // TAMAÑO_CELDA
        sel = self.seleccion.get()

        if self.fase == FASE_DEF:
            if sel == "muro":
                ok, msg = self.juego.comprar_muro(fila, col)
            else:
                ok, msg = self.juego.comprar_torre(sel, fila, col)
        elif self.fase == FASE_ATK:
            ok, msg = self.juego.comprar_unidad(sel, fila, col)
        else:
            return

        color_msg = "#00cc66" if ok else "#ff4444"
        self.lbl_msg.config(text=msg, fg=color_msg)
        self._actualizar_panel()
        self.dibujar_mapa()

    def _terminar_fase(self):
        if self.fase == FASE_DEF:
            self.fase = FASE_ATK
            self._actualizar_panel()
            self.lbl_msg.config(text="Turno del atacante. Coloca unidades en el borde.",
                                 fg="#ffcc00")

        elif self.fase == FASE_ATK:
            # Verificar si el atacante se quedó sin dinero y sin unidades
            if self.juego.atacante_sin_recursos():
                self.lbl_msg.config(
                    text="El atacante no tiene dinero ni unidades. Defensor gana la ronda.",
                    fg="#ff4444")
                self.fase = FASE_COM
                self._actualizar_panel()
                self.btn_terminar.config(state="disabled")
                self.root.after(500, self._ejecutar_combate)
                return
            self.fase = FASE_COM
            self._actualizar_panel()
            self.btn_terminar.config(state="disabled")
            self.lbl_msg.config(text="Ejecutando combate...", fg="#ffcc00")
            self.root.after(300, self._ejecutar_combate)

    def _ejecutar_combate(self):
        ganador_ronda = self.juego.ejecutar_combate()
        self.juego.registrar_victoria_ronda(ganador_ronda)
        self.dibujar_mapa()
        self._actualizar_panel()

        # Mostrar log
        top = tk.Toplevel(self.root)
        top.title("Resultado del combate")
        top.configure(bg=COLORES["bg"])
        top.geometry("420x400")
        centrar(top, 420, 420)

        quien = "DEFENSOR" if ganador_ronda == "defensor" else "ATACANTE"
        mk_label(top, f"✦ Ganó el {quien} ✦", size=13, bold=True,
                 color=COLORES["boton"], bg=COLORES["bg"]).pack(pady=(12, 6))

        txt = tk.Text(top, bg=COLORES["entrada"], fg=COLORES["texto"],
                      font=("Consolas", 8), relief="flat", wrap="word")
        txt.pack(fill="both", expand=True, padx=12, pady=6)
        txt.insert("end", "\n".join(self.juego.log))
        txt.config(state="disabled")

        def cerrar_y_continuar():
            top.destroy()
            ganador_partida, rol = self.juego.hay_ganador_partida()
            if ganador_partida:
                ganador_partida.agregar_victoria(rol)
                self.frame.destroy()
                centrar(self.root, 520, 400)
                PantallaFin(self.root, ganador_partida, rol)
            else:
                self.juego.iniciar_nueva_ronda()
                self.fase = FASE_DEF
                self.btn_terminar.config(state="normal")
                self._actualizar_panel()
                self.dibujar_mapa()
                self.lbl_msg.config(text=f"Ronda {self.juego.ronda_actual}. Turno del defensor.",
                                    fg="#ffcc00")

        mk_btn(top, "Continuar", cerrar_y_continuar, ancho=16).pack(pady=8)

    def _ver_ranking(self):
        top = tk.Toplevel(self.root)
        top.title("Ranking de Jugadores")
        top.configure(bg=COLORES["bg"])
        centrar(top, 480, 360)
        _construir_ranking(top)


# ── Pantalla Fin ───────────────────────────────────────────────

class PantallaFin:
    def __init__(self, root, ganador, rol):
        self.root = root
        self.ganador = ganador
        self.rol = rol

        self.frame = tk.Frame(root, bg=COLORES["bg"])
        self.frame.pack(fill="both", expand=True, padx=30, pady=30)

        mk_titulo(self.frame, "🏆  PARTIDA TERMINADA  🏆", 15).pack(pady=(20, 10))
        mk_label(self.frame, f"¡Ganó {ganador.nombre_usuario}!", size=14, bold=True,
                 color="#FFD700", bg=COLORES["bg"]).pack(pady=6)
        mk_label(self.frame, f"Rol: {rol.capitalize()}", size=11,
                 color=COLORES["subtexto"], bg=COLORES["bg"]).pack(pady=4)
        mk_label(self.frame,
                 f"Victorias como defensor: {ganador.victorias_defensor}",
                 size=10, bg=COLORES["bg"]).pack()
        mk_label(self.frame,
                 f"Victorias como atacante:  {ganador.victorias_atacante}",
                 size=10, bg=COLORES["bg"]).pack(pady=(0, 20))

        mk_btn(self.frame, "Ver Ranking", self._ver_ranking, ancho=20).pack(pady=6)
        mk_btn(self.frame, "Jugar de nuevo", self._jugar_nuevo,
               color=COLORES["boton2"], ancho=20).pack(pady=6)

    def _ver_ranking(self):
        top = tk.Toplevel(self.root)
        top.title("Ranking")
        top.configure(bg=COLORES["bg"])
        centrar(top, 480, 360)
        _construir_ranking(top)

    def _jugar_nuevo(self):
        self.frame.destroy()
        centrar(self.root, 520, 570)
        PantallaLogin(self.root)


# ── Ranking ────────────────────────────────────────────────────

def _construir_ranking(parent):
    mk_label(parent, "🏅  TOP JUGADORES  🏅", size=13, bold=True,
             color=COLORES["boton"], bg=COLORES["bg"]).pack(pady=(14, 10))

    container = tk.Frame(parent, bg=COLORES["bg"])
    container.pack(fill="both", expand=True, padx=20)

    j_temp = Jugador("_", "_")
    for col_idx, (titulo_col, rol) in enumerate([("🛡 Defensores", "defensor"),
                                                  ("⚔ Atacantes",  "atacante")]):
        frame_col = tk.Frame(container, bg=COLORES["panel"],
                             highlightthickness=1, highlightbackground=COLORES["borde"])
        frame_col.grid(row=0, column=col_idx, padx=10, sticky="nsew")
        container.columnconfigure(col_idx, weight=1)

        mk_label(frame_col, titulo_col, size=11, bold=True,
                 color=COLORES["boton"]).pack(pady=(10, 6))

        top5 = j_temp.obtener_top(rol, 5)
        if not top5:
            mk_label(frame_col, "Sin registros", size=9,
                     color=COLORES["subtexto"]).pack(pady=4)
        else:
            for pos, entry in enumerate(top5, 1):
                texto = f"{pos}. {entry['nombre']:<14} {entry['victorias']} V"
                mk_label(frame_col, texto, size=9).pack(anchor="w", padx=12, pady=2)

    mk_btn(parent, "Cerrar", parent.destroy, color=COLORES["boton2"], ancho=14).pack(pady=12)


# ── Entry Point ────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    PantallaLogin(root)
    root.mainloop()
