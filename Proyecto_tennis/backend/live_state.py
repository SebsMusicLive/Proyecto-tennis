# backend/live_state.py

import reflex as rx
from ..backend.api_client import get_live_matches

class LiveMatchState(rx.State):
    matches: list[dict] = []

    def load_matches(self):
        data = get_live_matches()
        self.matches = data.get("events", [])
