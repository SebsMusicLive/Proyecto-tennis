"""The overview page of the app."""

import reflex as rx
from .. import styles
from ..templates import template
from ..components.card import card
from ..backend.live_state import LiveMatchState


# --- Función para renderizar una tarjeta de partido ---
def render_match_card(match: rx.Var) -> rx.Component:
    # Todos los porcentajes y estadísticas ya vienen calculados y formateados como strings desde live_state.py

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.cond(
                    (match.HOME_IMAGES != None) & (match.HOME_IMAGES.length() > 0),
                    rx.image(src=match.HOME_IMAGES[0], width="50px", height="50px", border_radius="full"),
                    rx.icon("circle-user", size=24) 
                ),
                rx.text(f"{match.HOME_NAME} vs {match.AWAY_NAME}", weight="bold", size="5"),
                spacing="4",
                align="center"
            ),
            
            rx.text(f"🎾 Torneo: {match.TOURNAMENT_NAME} ({match.TOURNAMENT_YEAR})", size="3"),
            rx.text(f"🌍 País Local: {match.HOME_COUNTRY}", size="3"),
            rx.text(f"🌍 País Visitante: {match.AWAY_COUNTRY}", size="3"), 
            rx.text(f"📌 Estado: {match.MATCH_STATUS} ({match.STATUS_TYPE})", size="3"),
            rx.text(f"🔁 Ronda: {match.ROUND}", size="3"),
            # La línea para la hora de inicio ya fue eliminada en la revisión anterior.

            rx.divider(), 

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

            # 🚨🚨🚨 SECCIÓN "Historial (H2H)" ELIMINADA COMPLETAMENTE 🚨🚨🚨
            # Este divider y el texto del historial ya NO estarán.
            # rx.divider(), 
            # rx.text("📊 Historial (H2H):", size="3", weight="medium", align_self="flex-start"),
            # rx.text("No hay historial Head-to-Head disponible para esta API.", size="2", color="gray.500"),


            rx.divider(), # Separador para estadísticas del partido actual

            # --- Estadísticas del Partido Actual ---
            rx.text("📈 Estadísticas del Partido:", size="3", weight="medium", align_self="flex-start"),
            rx.vstack(
                rx.hstack(
                    rx.text("Aces:", weight="bold", size="2"),
                    rx.spacer(),
                    rx.text(f"{match.HOME_ACES} - {match.AWAY_ACES}", size="2"),
                    width="100%"
                ),
                rx.hstack(
                    rx.text("Dobles faltas:", weight="bold", size="2"),
                    rx.spacer(),
                    rx.text(f"{match.HOME_DOUBLE_FAULTS} - {match.AWAY_DOUBLE_FAULTS}", size="2"),
                    width="100%"
                ),
                rx.hstack(
                    rx.text("Puntos de quiebre ganados:", weight="bold", size="2"),
                    rx.spacer(),
                    rx.text(f"{match.HOME_BREAKPOINTS_WON} - {match.AWAY_BREAKPOINTS_WON}", size="2"),
                    width="100%"
                ),
                rx.hstack(
                    rx.text("1er Saque Exitoso (Cant.):", weight="bold", size="2"),
                    rx.spacer(),
                    rx.text(f"{match.HOME_FIRST_SERVE_SUCCESSFUL} - {match.AWAY_FIRST_SERVE_SUCCESSFUL}", size="2"),
                    width="100%"
                ),
                rx.hstack(
                    rx.text("Puntos de Servicio Ganados (Cant.):", weight="bold", size="2"),
                    rx.spacer(),
                    rx.text(f"{match.HOME_SERVICE_POINTS_WON} - {match.AWAY_SERVICE_POINTS_WON}", size="2"),
                    width="100%"
                ),

                rx.divider(size="1"), # Separador para porcentajes de éxito

                rx.text("Porcentajes de Éxito:", size="3", weight="bold", align_self="flex-start", margin_top="0.5em"),
                rx.hstack(
                    rx.text("1er Saque Ganado (Pts.):", weight="bold", size="2"),
                    rx.spacer(),
                    rx.text(f"{match.HOME_FIRST_SERVE_WIN_PERCENTAGE} - {match.AWAY_FIRST_SERVE_WIN_PERCENTAGE}", size="2"),
                    width="100%"
                ),
                rx.hstack(
                    rx.text("Puntos de Servicio Ganados (Total):", weight="bold", size="2"),
                    rx.spacer(),
                    rx.text(f"{match.HOME_SERVICE_POINTS_WIN_PERCENTAGE} - {match.AWAY_SERVICE_POINTS_WIN_PERCENTAGE}", size="2"),
                    width="100%"
                ),
                rx.hstack(
                    rx.text("Quiebres Convertidos:", weight="bold", size="2"),
                    rx.spacer(),
                    rx.text(f"{match.HOME_BREAKPOINT_CONVERSION_PERCENTAGE} - {match.AWAY_BREAKPOINT_CONVERSION_PERCENTAGE}", size="2"),
                    width="100%"
                ),
                align_items="flex-start",
                spacing="1",
                width="100%",
                padding_left="1em",
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