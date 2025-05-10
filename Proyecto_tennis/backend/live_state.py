# backend/live_state.py

import reflex as rx
import datetime
from ..backend.api_client import get_live_matches

# ✅ Definir un modelo para un partido
class Match(rx.Base):
    HOME_NAME: str
    AWAY_NAME: str
    ROUND: str
    START_TIME: int
    FORMATTED_TIME: str = "Sin hora"
    HOME_IMAGES: list[str] = []

class LiveMatchState(rx.State):
    matches: list[Match] = []

    def load_matches(self):
        data = get_live_matches()
        raw_matches = data.get("events", [])

        parsed_matches = []

        for match in raw_matches:
            try:
                ts = match.get("START_TIME", 0)
                formatted_time = (
                    datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M') if ts else "Sin hora"
                )

                parsed_matches.append(
                    Match(
                        HOME_NAME=match.get("HOME_NAME", ""),
                        AWAY_NAME=match.get("AWAY_NAME", ""),
                        ROUND=match.get("ROUND", ""),
                        START_TIME=ts,
                        FORMATTED_TIME=formatted_time,
                        HOME_IMAGES=match.get("HOME_IMAGES", []),
                    )
                )
            except Exception:
                continue

        self.matches = parsed_matches
