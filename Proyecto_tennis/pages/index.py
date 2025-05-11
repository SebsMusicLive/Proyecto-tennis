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
    home = match.HOME_NAME
    away = match.AWAY_NAME
    round_name = match.ROUND
    date_display = match.FORMATTED_TIME  # Usar formato legible aquí si quieres
    image_list = match.HOME_IMAGES

    return rx.box(
        rx.hstack(
            rx.cond(
                (image_list != None) & (image_list.length() > 0),
                rx.image(src=image_list[0], width="50px", height="50px", border_radius="full"),
                rx.icon("circle-user")
            ),
            rx.vstack(
                rx.text(f"{home} vs {away}", weight="bold"),
                rx.text(f"Ronda: {round_name}"),
                rx.text(f"Inicio: {date_display}"),
            ),
            align="start",
            spacing="4",
        ),
        padding="1em",
        border="1px solid #ccc",
        border_radius="lg",
        box_shadow="md",
        width="100%",
    )


@template(route="/", title="Estadísticas", on_load=LiveMatchState.load_matches)
def index() -> rx.Component:
    return rx.vstack(
        rx.heading("BIENVENIDO A PAGINA DE ESTADISTICAS TENNIS EN VIVO", size="8", align="left"),
        stats_cards(),

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
                "repeat(1, 1fr)",
                "repeat(2, 1fr)",
                "repeat(2, 1fr)",
                "repeat(2, 1fr)",
            ],
            spacing="8",
            width="100%",
        ),
    )
