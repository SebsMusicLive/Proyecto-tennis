"""The overview page of the app."""

import reflex as rx
from .. import styles
from ..backend.table_state import TableState, Item
from ..templates import template
# from ..views.stats_cards import stats_cards 
# from ..views.charts import ( 
#     users_chart,
#     revenue_chart,
#     orders_chart,
#     area_toggle,
#     pie_chart,
#     timeframe_select,
#     StatsState,
# )
# from ..views.adquisition_view import adquisition 
from ..components.notification import notification
from ..components.card import card
from ..backend.live_state import LiveMatchState


# --- Función para renderizar una tarjeta de partido ---
def render_match_card(match: rx.Var) -> rx.Component:
    # Los porcentajes H2H ya se calculan y formatean en live_state.py
    # No es necesario calcularlos aquí ni usar .to_fixed() en el frontend
    # h2h_total_matches = match.HEAD_TO_HEAD_TOTAL_MATCHES 
    # h2h_home_win_percentage = rx.cond(...)
    # h2h_away_win_percentage = rx.cond(...)

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
            rx.text(f"⏰ Inicio: {match.FORMATTED_TIME}", size="3"),

            rx.divider(), 

            rx.hstack(
                rx.icon("git-commit", size=20), 
                rx.text(f"Set Actual: {match.CURRENT_SET}", size="3", weight="medium"),
                rx.spacer(),
                rx.text(f"Sets: {match.HOME_SCORE_CURRENT_SET} - {match.AWAY_SCORE_CURRENT_SET}", size="3", weight="bold"),
                spacing="2",
                align="center",
                width="100%"
            ),
            
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

            rx.divider(),

            # --- Estadísticas Head-to-Head (H2H) ---
            rx.text("📊 Historial (H2H):", size="3", weight="medium", align_self="flex-start"),
            rx.cond(
                match.HEAD_TO_HEAD_TOTAL_MATCHES > 0,
                rx.vstack(
                    rx.text(f"Partidos jugados: {match.HEAD_TO_HEAD_TOTAL_MATCHES}", size="2"),
                    # 🚨 USAR LOS CAMPOS YA CALCULADOS Y FORMATEADOS
                    rx.text(f"{match.HOME_NAME}: {match.HEAD_TO_HEAD_WINS_HOME} victorias ({match.HOME_WIN_PERCENTAGE_H2H}%)", size="2"),
                    rx.text(f"{match.AWAY_NAME}: {match.HEAD_TO_HEAD_WINS_AWAY} victorias ({match.AWAY_WIN_PERCENTAGE_H2H}%)", size="2"),
                    align_items="flex-start",
                    spacing="1",
                    width="100%"
                ),
                rx.text("No hay historial Head-to-Head disponible.", size="2", color="gray.500")
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
                )
            ),
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "1fr",
                "1fr 1fr"
            ],
            spacing="8",
            width="100%",
        ),
        width="100%",
        padding_x=styles.PAGE_PADDING_X,
        padding_y=styles.PAGE_PADDING_Y,
        align_items="flex-start"
    )