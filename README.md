# Defensa y Asalto de Base
**Curso:** Introducción a la Programación — TEC Campus San Carlos  
**Lenguaje:** Python 3 | **Interfaz:** Tkinter

## Integrantes
- David Zamora Villalobos
- Josué Solano Monje

## Cómo ejecutar
```bash
pip install Pillow
python main.py
```

## Estructura de archivos
```
Proyecto_2_Defensa_Asalto_Base/
├── main.py              ← Punto de entrada (ejecutar esto)
├── jugadores.json       ← Base de datos de jugadores
├── README.md
├── Assets/              ← Imágenes de torres y unidades por facción
│   ├── Imperio/
│   ├── Rebeldes/
│   └── Reinado/
└── python/
    ├── __init__.py
    ├── torre.py         ← Torre, TorreBasica, TorrePesada, TorreMagica, Muro, Base
    ├── unidad.py        ← Unidad, Soldado, Tanque, UnidadRapida
    ├── jugador.py       ← Registro, login, victorias, ranking
    ├── juego.py         ← Lógica de rondas, combate, dinero
    └── imagenes.py      ← Carga de imágenes de torres/unidades por facción
```

## Instrucciones del juego
1. Ambos jugadores se registran o inician sesión.
2. Cada uno elige una facción distinta (imperio, rebeldes, reinado).
3. **Fase Defensor:** coloca torres y muros haciendo click en el mapa.
4. **Fase Atacante:** coloca unidades en el borde del mapa.
5. El combate se ejecuta automáticamente.
6. Gana 3 rondas para ganar la partida.

## Facciones
| Facción | Color de respaldo | Estilo visual |
|---|---|---|
| Imperio | Café | Torres oscuras de piedra, unidades tipo criatura/anime |
| Rebeldes | Verde | Castillo natural, unidades con capucha |
| Reinado | Azul acero | Torres clásicas de fantasía con bandera |

Cada facción tiene imágenes propias para sus 3 tipos de torre y sus 3 tipos de unidad,
ubicadas en `Assets/<Facción>/`. Si una imagen no se encuentra, el juego usa
automáticamente el color de respaldo de la facción (no se rompe el juego).

## Torres
| Torre | Costo | Vida | Daño | Alcance | Habilidad |
|---|---|---|---|---|---|
| Básica | $50 | 80 | 15 | 3 | Disparo Doble (cada 3 turnos) |
| Pesada | $150 | 200 | 40 | 2 | Daño en Área (cada 4 turnos) |
| Mágica | $100 | 60 | 10 | 4 | Congelar (cada 3 turnos) |

## Unidades
| Unidad | Costo | Vida | Daño | Velocidad | Habilidad |
|---|---|---|---|---|---|
| Soldado | $30 | 60 | 10 | 1 | Ataque Doble |
| Tanque | $120 | 200 | 25 | 1 | Escudo Temporal |
| Unidad Rápida | $60 | 40 | 8 | 3 | Aumento de Velocidad |

## Repositorio
https://github.com/JosueSolano2008/Proyecto_2_Defensa_Asalto_Base

## Trabajo realizado
Este proyecto fue desarrollado en conjunto por ambos integrantes de la pareja.
El diseño de las clases de torres, unidades y jugador (estadísticas, costos y
habilidades especiales) y las imágenes de las facciones Imperio, Rebeldes y
Reinado fueron desarrollados conjuntamente. La integración final del motor
de juego (mapa, rondas, combate, economía), la interfaz gráfica en Tkinter
y la incorporación de las imágenes al mapa también fueron trabajo conjunto.
