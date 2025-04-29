"""The table page."""

from ..templates import template
from ..backend.table_state import TableState
from ..views.table import main_table

import reflex as rx


@template(route="/table", title="Posiciones", on_load=TableState.load_entries)
def table() -> rx.Component:
    """The table page.

    Returns:
        The UI for the table page.
    """
    return rx.vstack(
        rx.heading("HISTORICO JUGADORES", size="5"),
        main_table(),
        spacing="8",
        width="100%",
    )
