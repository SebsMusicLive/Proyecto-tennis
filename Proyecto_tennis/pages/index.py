"""The overview page of the app."""

import reflex as rx
from .. import styles
from ..backend.table_state import TableState, Item
from ..templates import template
from ..views.stats_cards import stats_cards
from ..views.charts import (
    users_chart,
    revenue_chart,
    orders_chart,
    area_toggle,
    pie_chart,
    timeframe_select,
    StatsState,
)
from ..views.adquisition_view import adquisition
from ..components.notification import notification
from ..components.card import card
from ..backend.live_state import LiveMatchState


def render_match_card(match: rx.Var) -> rx.Component:
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
            rx.text(f"🌍 País del jugador local: {match.HOME_COUNTRY}", size="3"),
            rx.text(f"📌 Estado del partido: {match.MATCH_STATUS} ({match.STATUS_TYPE})", size="3"),
            rx.text(f"🔁 Ronda: {match.ROUND}", size="3"),
            rx.text(f"⏰ Inicio: {match.FORMATTED_TIME}", size="3"),
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
        rx.heading("BIENVENIDO A PAGINA DE ESTADISTICAS TENNIS EN VIVO", size="8", align="left"),
        #stats_cards(),

        rx.grid(
            # Partidos en vivo
            card(
                rx.hstack(
                    rx.icon("circle-help", size=20),
                    rx.text("Partidos en Vivo", size="4", weight="medium"),
                    align="center",
                    spacing="2",
                ),
                rx.foreach(LiveMatchState.matches, render_match_card),

            ),
            gap="1rem",
            grid_template_columns=[
    "1fr",
    "1fr",
    "1fr",
]
,
            spacing="8",
            width="100%",
        ),
    )
