"""The overview page of the app."""

import reflex as rx
from .. import styles
from ..templates import template
from ..components.card import card
from ..backend.live_state import LiveMatchState


# --- Función para renderizar una tarjeta de partido ---
def render_match_card(match: rx.Var) -> rx.Component:
    return rx.box(
        rx.vstack(
            # --- SECCIÓN SUPERIOR: Nombres de Jugadores y Países ---
            rx.hstack(
                # Jugador Local (Izquierda)
                rx.vstack(
                    rx.hstack(
                        rx.cond(
                            (match.HOME_IMAGES != None) & (match.HOME_IMAGES.length() > 0),
                            rx.image(src=match.HOME_IMAGES[0], width="40px", height="40px", border_radius="full", margin_right="0.5em"),
                            rx.icon("circle-user", size=20, margin_right="0.5em")
                        ),
                        rx.text(match.HOME_NAME, weight="bold", size="4"),
                        align="center",
                    ),
                    rx.text(f"🌍 {match.HOME_COUNTRY}", size="2", color="gray.400"),
                    align_items="flex-start",
                    spacing="1",
                ),
                
                rx.spacer(), 
                
                # Símbolo "vs" (Centrado)
                rx.center(
                    rx.text("vs", weight="bold", size="3", color="gray.600"),
                    width="40px", 
                ),

                rx.spacer(), 

                # Jugador Visitante (Derecha)
                rx.vstack(
                    rx.hstack(
                        rx.text(match.AWAY_NAME, weight="bold", size="4"),
                        rx.cond(
                            (match.HOME_IMAGES != None) & (match.HOME_IMAGES.length() > 0), # Reemplaza por AWAY_IMAGES si lo implementas
                            rx.image(src=match.HOME_IMAGES[0], width="40px", height="40px", border_radius="full", margin_left="0.5em"),
                            rx.icon("circle-user", size=20, margin_left="0.5em")
                        ),
                        align="center",
                    ),
                    rx.text(f"🌍 {match.AWAY_COUNTRY}", size="2", color="gray.400"),
                    align_items="flex-end", 
                    spacing="1",
                ),
                width="100%",
                align="center",
                padding_bottom="1em", 
            ),

            # --- INFORMACIÓN GENERAL CENTRALIZADA: Torneo, Estado, Ronda ---
            # 🚨 CAMBIO AQUÍ: Aseguramos que el vstack interno también centre su contenido
            rx.vstack( # Mantén este vstack para agrupar los elementos
                rx.text(f"🎾 Torneo: {match.TOURNAMENT_NAME} ({match.TOURNAMENT_YEAR})", size="3", text_align="center", width="100%"), # Asegura width="100%"
                rx.text(f"📌 Estado: {match.MATCH_STATUS} ({match.STATUS_TYPE})", size="3", text_align="center", width="100%"),
                rx.text(f"🔁 Ronda: {match.ROUND}", size="3", text_align="center", width="100%"),
                spacing="1",
                align_items="center", # 🚨 Asegura que los items dentro del vstack se centren
                width="100%", # Asegura que el vstack ocupe todo el ancho disponible
            ),


            rx.divider(margin_y="1em"), 

            # --- Información del Set y Puntuación Actual ---
            rx.hstack(
                rx.icon("git-commit", size=20), 
                rx.text(f"Set Actual: {match.CURRENT_SET}", size="3", weight="medium"),
                rx.spacer(), 
                rx.text(f"Sets: {match.HOME_SCORE_CURRENT_SET} - {match.AWAY_SCORE_CURRENT_SET}", size="3", weight="bold"),
                spacing="2",
                align="center",
                width="100%"
            ),
            
            # Puntuación del juego actual (0, 15, 30, 40)
            rx.hstack(
                rx.icon("dices", size=20), 
                rx.text(f"Puntos: {match.GAME_STATE_HOME_SCORE} - {match.GAME_STATE_AWAY_SCORE}", size="3", weight="medium"),
                rx.spacer(),
                rx.cond(
                    match.SERVING_PLAYER == "home",
                    rx.text(f"Sirve: {match.HOME_NAME}", size="3", color="green.300"),
                    rx.cond(
                        match.SERVING_PLAYER == "away",
                        rx.text(f"Sirve: {match.AWAY_NAME}", size="3", color="red.300"),
                        rx.text("Sirve: Desconocido", size="3")
                    )
                ),
                spacing="2",
                align="center",
                width="100%"
            ),

            rx.divider(margin_y="1em"), 

            # --- ESTADÍSTICAS DEL PARTIDO ACTUAL: VALORES A LOS EXTREMOS, TÍTULO EN EL MEDIO ---
            rx.text("📈 Estadísticas del Partido:", size="3", weight="medium", align_self="flex-start", padding_bottom="0.5em"),
            rx.vstack( 
                # Fila de Aces
                rx.hstack(
                    rx.text(match.HOME_ACES, size="3", weight="bold", color=rx.color("blue", 7)), 
                    rx.spacer(),
                    rx.text("Aces", size="2", weight="medium", text_align="center"), 
                    rx.spacer(),
                    rx.text(match.AWAY_ACES, size="3", weight="bold", color=rx.color("red", 7)), 
                    width="100%",
                    align="center",
                ),
                rx.divider(size="1", margin_y="0.2em"), 

                # Fila de Dobles Faltas
                rx.hstack(
                    rx.text(match.HOME_DOUBLE_FAULTS, size="3", weight="bold", color=rx.color("blue", 7)),
                    rx.spacer(),
                    rx.text("Dobles faltas", size="2", weight="medium", text_align="center"),
                    rx.spacer(),
                    rx.text(match.AWAY_DOUBLE_FAULTS, size="3", weight="bold", color=rx.color("red", 7)),
                    width="100%",
                    align="center",
                ),
                rx.divider(size="1", margin_y="0.2em"),

                # Fila de Puntos de Quiebre Ganados
                rx.hstack(
                    rx.text(match.HOME_BREAKPOINTS_WON, size="3", weight="bold", color=rx.color("blue", 7)),
                    rx.spacer(),
                    rx.text("Puntos de quiebre ganados", size="2", weight="medium", text_align="center"),
                    rx.spacer(),
                    rx.text(match.AWAY_BREAKPOINTS_WON, size="3", weight="bold", color=rx.color("red", 7)),
                    width="100%",
                    align="center",
                ),
                rx.divider(size="1", margin_y="0.2em"),

                # Fila de 1er Saque Exitoso (Cantidad)
                rx.hstack(
                    rx.text(match.HOME_FIRST_SERVE_SUCCESSFUL, size="3", weight="bold", color=rx.color("blue", 7)),
                    rx.spacer(),
                    rx.text("1er Saque Exitoso (Cant.)", size="2", weight="medium", text_align="center"),
                    rx.spacer(),
                    rx.text(match.AWAY_FIRST_SERVE_SUCCESSFUL, size="3", weight="bold", color=rx.color("red", 7)),
                    width="100%",
                    align="center",
                ),
                rx.divider(size="1", margin_y="0.2em"),

                # Fila de Puntos de Servicio Ganados (Cantidad)
                rx.hstack(
                    rx.text(match.HOME_SERVICE_POINTS_WON, size="3", weight="bold", color=rx.color("blue", 7)),
                    rx.spacer(),
                    rx.text("Puntos de Servicio Ganados (Cant.)", size="2", weight="medium", text_align="center"),
                    rx.spacer(),
                    rx.text(match.AWAY_SERVICE_POINTS_WON, size="3", weight="bold", color=rx.color("red", 7)),
                    width="100%",
                    align="center",
                ),

                rx.divider(size="2", margin_y="1em"), 

                rx.text("Porcentajes de Éxito:", size="3", weight="bold", align_self="flex-start"),
                
                # Fila de Porcentaje 1er Saque Ganado
                rx.hstack(
                    rx.text(match.HOME_FIRST_SERVE_WIN_PERCENTAGE, size="3", weight="bold", color=rx.color("blue", 7)),
                    rx.spacer(),
                    rx.text("1er Saque Ganado (Pts.)", size="2", weight="medium", text_align="center"),
                    rx.spacer(),
                    rx.text(match.AWAY_FIRST_SERVE_WIN_PERCENTAGE, size="3", weight="bold", color=rx.color("red", 7)),
                    width="100%",
                    align="center",
                ),
                rx.divider(size="1", margin_y="0.2em"),

                # Fila de Porcentaje Puntos de Servicio Ganados
                rx.hstack(
                    rx.text(match.HOME_SERVICE_POINTS_WIN_PERCENTAGE, size="3", weight="bold", color=rx.color("blue", 7)),
                    rx.spacer(),
                    rx.text("Puntos de Servicio Ganados (Total)", size="2", weight="medium", text_align="center"),
                    rx.spacer(),
                    rx.text(match.AWAY_SERVICE_POINTS_WIN_PERCENTAGE, size="3", weight="bold", color=rx.color("red", 7)),
                    width="100%",
                    align="center",
                ),
                rx.divider(size="1", margin_y="0.2em"),

                # Fila de Porcentaje Quiebres Convertidos
                rx.hstack(
                    rx.text(match.HOME_BREAKPOINT_CONVERSION_PERCENTAGE, size="3", weight="bold", color=rx.color("blue", 7)),
                    rx.spacer(),
                    rx.text("Quiebres Convertidos", size="2", weight="medium", text_align="center"),
                    rx.spacer(),
                    rx.text(match.AWAY_BREAKPOINT_CONVERSION_PERCENTAGE, size="3", weight="bold", color=rx.color("red", 7)),
                    width="100%",
                    align="center",
                ),
                align_items="flex-start",
                spacing="1",
                width="100%",
                padding_left="1em",
                padding_right="1em", 
            ),
        ),
        padding="1em",
        border="1px solid #3d3d3d",
        border_radius="xl",
        box_shadow="lg",
        background_color="#1a1a1a",
        width="100%", 
        _hover={"box_shadow": "0 0 0 2px #ff4081"},
        transition="all 0.3s ease-in-out",
    )

@template(route="/", title="Estadísticas", on_load=LiveMatchState.load_matches)
def index() -> rx.Component:
    return rx.vstack(
        rx.heading("BIENVENIDO A PÁGINA DE ESTADÍSTICAS TENNIS EN VIVO", size="8", align="left"),
        
        rx.grid(
            card( 
                rx.hstack(
                    rx.icon("circle-help", size=20),
                    rx.text("Partidos en Vivo", size="4", weight="medium"),
                    align="center",
                    spacing="2",
                    justify="start", 
                    width="100%"
                ),
                rx.spacer(), 
                rx.scroll_area(
                    rx.vstack(
                        rx.foreach(LiveMatchState.matches, render_match_card),
                        spacing="4",
                        align_items="stretch", 
                        width="100%", 
                        padding="0.5em"
                    ),
                    type="always", 
                    scrollbars="both", 
                    style={"height": "600px", "width": "100%"}, 
                ),
                col_span="all", 
            ),
            gap="1rem", 
            grid_template_columns=[
                "1fr", 
                "1fr", 
                "1fr" 
            ],
            width="100%", 
            spacing="8",
        ),
        width="100%", 
        padding_x=styles.PAGE_PADDING_X, 
        padding_y=styles.PAGE_PADDING_Y, 
        align_items="flex-start" 
    )