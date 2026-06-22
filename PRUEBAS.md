# Evidencia de pruebas

## Flujo principal
- Registro de dos jugadores.
- Inicio de sesión de ambos jugadores.
- Selección de facciones distintas.
- Fase defensor con torres y muros.
- Fase atacante con unidades colocadas en el borde.
- Combate automático.
- Finalización de partida al ganar 3 rondas.
- Pantalla final con ganador.
- Ranking de defensores y atacantes.

## Casos validados
- Usuario duplicado.
- Contraseña incorrecta.
- Usuario inexistente.
- Facciones iguales bloqueadas.
- Selección de facción incompleta bloqueada.
- Colocación sobre celda ocupada bloqueada.
- Dinero insuficiente bloqueado.
- Unidades fuera del borde bloqueadas.
- Botón "Jugar de nuevo".

## Correcciones verificadas
- La animación del mapa no genera errores al cambiar a pantalla final.
- La base y los muros cambian visualmente según la facción defensora.
- El defensor recibe dinero al eliminar unidades en el combate visual.
- La terminal queda limpia de mensajes internos de habilidades.
