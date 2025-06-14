# backend/live_state.py

import reflex as rx
import datetime
import json
from ..backend.api_client import get_live_matches, get_head_to_head_stats 

class Match(rx.Base):
    HOME_NAME: str
    AWAY_NAME: str
    ROUND: str
    START_TIME: int
    FORMATTED_TIME: str = "Sin hora"
    HOME_IMAGES: list[str] = [] 

    TOURNAMENT_NAME: str = ""
    TOURNAMENT_YEAR: str = ""
    MATCH_STATUS: str = ""      
    STATUS_TYPE: str = ""       
    HOME_COUNTRY: str = ""
    AWAY_COUNTRY: str = ""

    HOME_ID: str = "" 
    AWAY_ID: str = ""
    CURRENT_SET: int = 0
    HOME_SCORE_CURRENT_SET: int = 0
    AWAY_SCORE_CURRENT_SET: int = 0
    GAME_STATE_HOME_SCORE: int = 0 
    GAME_STATE_AWAY_SCORE: int = 0
    SERVING_PLAYER: str = "" 

    HEAD_TO_HEAD_WINS_HOME: int = 0
    HEAD_TO_HEAD_WINS_AWAY: int = 0
    HEAD_TO_HEAD_TOTAL_MATCHES: int = 0
    WIN_PROBABILITY_HOME: float = 0.0 
    WIN_PROBABILITY_AWAY: float = 0.0
    
    # NUEVOS CAMPOS: Porcentajes calculados y formateados como cadenas
    HOME_WIN_PERCENTAGE_H2H: str = "N/A"
    AWAY_WIN_PERCENTAGE_H2H: str = "N/A"

class LiveMatchState(rx.State):
    matches: list[Match] = []

    def load_matches(self):
        data = get_live_matches() 

        raw_matches = data.get("summaries", [])

        parsed_matches = []

        if not raw_matches:
            print("ℹ️ No se encontraron resúmenes de partidos en vivo de Sportradar.")
            self.matches = []
            return

        # 🟡 DEBUG: Imprimir la estructura del primer partido que se procesa
        # print("\n🔍 Estructura del primer resumen de partido (datos crudos de Sportradar):")
        # if raw_matches: 
        #     print(json.dumps(raw_matches[0], indent=2)) 
        # print("----------------------------------------------------\n")

        try:
            for match_summary in raw_matches:

                sport_event = match_summary.get("sport_event", {})
                sport_event_status = match_summary.get("sport_event_status", {})
                sport_event_context = sport_event.get("sport_event_context", {}) 

                competitors = sport_event.get("competitors", [])
                
                home_data = next((c for c in competitors if c.get("qualifier") == "home"), {})
                away_data = next((c for c in competitors if c.get("qualifier") == "away"), {})

                home_name = home_data.get("name", "Desconocido")
                away_name = away_data.get("name", "Desconocido")
                
                home_country = home_data.get("country", "")
                away_country = away_data.get("country", "")

                home_id = home_data.get("id", "")
                away_id = away_data.get("id", "")

                round_data = sport_event_context.get("round", {})
                round_name = round_data.get("name", "Sin ronda") 

                tournament_name = sport_event_context.get("competition", {}).get("name", "Torneo Desconocido")
                tournament_year = str(sport_event_context.get("season", {}).get("year", datetime.datetime.now().year))
                
                start_time_iso = sport_event.get("start_time")
                ts = 0
                formatted_time = "Sin hora"
                if start_time_iso:
                    try:
                        dt_object = datetime.datetime.fromisoformat(start_time_iso.replace('Z', '+00:00'))
                        ts = int(dt_object.timestamp())
                        formatted_time = dt_object.astimezone(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
                    except ValueError:
                        print(f"⚠️ No se pudo parsear la fecha ISO: {start_time_iso}")

                match_status = sport_event_status.get("match_status", "Estado Desconocido")
                status_type = sport_event_status.get("status", "unknown")

                period_scores = sport_event_status.get("period_scores", [])
                current_set = len(period_scores) + 1 
                
                game_state = sport_event_status.get("game_state", {})
                home_score_current_game = game_state.get("home_score", 0)
                away_score_current_game = game_state.get("away_score", 0)
                serving_player = game_state.get("serving", "unknown")

                home_score_current_set = sport_event_status.get("home_score", 0) 
                away_score_current_set = sport_event_status.get("away_score", 0) 

                h2h_wins_home = 0
                h2h_wins_away = 0
                h2h_total_matches = 0
                home_win_percentage_h2h_str = "N/A"
                away_win_percentage_h2h_str = "N/A"

                if home_id and away_id:
                    h2h_data = get_head_to_head_stats(home_id, away_id)
                    if h2h_data:
                        if "head_to_head" in h2h_data:
                            h2h_summary = h2h_data["head_to_head"]
                            if h2h_summary.get("home_competitor_id") == home_id:
                                h2h_wins_home = h2h_summary.get("home_wins", 0)
                                h2h_wins_away = h2h_summary.get("away_wins", 0)
                            elif h2h_summary.get("home_competitor_id") == away_id: 
                                h2h_wins_home = h2h_summary.get("away_wins", 0)
                                h2h_wins_away = h2h_summary.get("home_wins", 0)
                            h2h_total_matches = h2h_summary.get("total_meetings", h2h_wins_home + h2h_wins_away)
                        elif "summaries" in h2h_data: 
                            for prev_match_summary in h2h_data["summaries"]:
                                if "sport_event_status" in prev_match_summary and "winner_id" in prev_match_summary["sport_event_status"]:
                                    winner_id = prev_match_summary["sport_event_status"]["winner_id"]
                                    if winner_id == home_id:
                                        h2h_wins_home += 1
                                    elif winner_id == away_id:
                                        h2h_wins_away += 1
                                    h2h_total_matches += 1
                        else:
                            print("⚠️ Estructura inesperada en la respuesta H2H. Imprime `h2h_data` para depurar.")

                # CALCULAR PORCENTAJES AQUÍ Y ALMACENAR COMO STRING
                if h2h_total_matches > 0:
                    home_win_percentage = (h2h_wins_home / h2h_total_matches) * 100
                    away_win_percentage = (h2h_wins_away / h2h_total_matches) * 100
                    home_win_percentage_h2h_str = f"{home_win_percentage:.1f}"
                    away_win_percentage_h2h_str = f"{away_win_percentage:.1f}"


                parsed_matches.append(
                    Match(
                        HOME_NAME=home_name,
                        AWAY_NAME=away_name,
                        ROUND=round_name,
                        START_TIME=ts,
                        FORMATTED_TIME=formatted_time,
                        HOME_IMAGES=[], 
                        TOURNAMENT_NAME=tournament_name,
                        TOURNAMENT_YEAR=tournament_year,
                        MATCH_STATUS=match_status,
                        STATUS_TYPE=status_type,
                        HOME_COUNTRY=home_country,
                        AWAY_COUNTRY=away_country,
                        HOME_ID=home_id, 
                        AWAY_ID=away_id,
                        CURRENT_SET=current_set,
                        HOME_SCORE_CURRENT_SET=home_score_current_set,
                        AWAY_SCORE_CURRENT_SET=away_score_current_set,
                        GAME_STATE_HOME_SCORE=home_score_current_game,
                        GAME_STATE_AWAY_SCORE=away_score_current_game,
                        SERVING_PLAYER=serving_player,
                        HEAD_TO_HEAD_WINS_HOME=h2h_wins_home,
                        HEAD_TO_HEAD_WINS_AWAY=h2h_wins_away,
                        HEAD_TO_HEAD_TOTAL_MATCHES=h2h_total_matches,
                        HOME_WIN_PERCENTAGE_H2H=home_win_percentage_h2h_str,
                        AWAY_WIN_PERCENTAGE_H2H=away_win_percentage_h2h_str
                    )
                )
        except Exception as e:
            print(f"❌ Error al procesar un resumen del partido de Sportradar: {e}")

        self.matches = parsed_matches

# --- Bloque de Prueba (main execution block, for isolated testing) ---
if __name__ == "__main__":
    # Mock para get_live_matches (ejemplo de respuesta real para summaries.json)
    def get_live_matches_sportradar_mock():
        return {
            "summaries": [ 
                {
                    "sport_event": {
                        "id": "sr:sport_event:61155415",
                        "start_time": "2025-06-14T02:15:00+00:00",
                        "start_time_confirmed": True,
                        "sport_event_context": {
                            "sport": {"id": "sr:sport:5", "name": "Tennis"},
                            "category": {"id": "sr:category:2516", "name": "UTR Men"},
                            "competition": {"id": "sr:competition:47205", "name": "UTR PTT Sanmin District Men 02", "type": "singles", "gender": "men"},
                            "season": {"id": "sr:season:131053", "name": "UTR Manchester M01 2025", "start_date": "2025-06-08", "end_date": "2025-06-14", "year": "2025", "competition_id": "sr:competition:47205"},
                            "stage": {"order": 2, "type": "cup", "phase": "stage_1_playoff", "start_date": "2025-06-13", "end_date": "2025-06-14", "year": "2025"},
                            "round": {"name": "semifinal"},
                            "groups": [{"id": "sr:cup:181943", "name": "2025 Sanmin District Men 02, 4th Place Playoffs"}],
                            "mode": {"best_of": 3}
                        },
                        "coverage": {
                            "type": "sport_event",
                            "sport_event_properties": {"enhanced_stats": False, "scores": "live", "detailed_serve_outcomes": True, "play_by_play": True}
                        },
                        "competitors": [
                            {"id": "sr:competitor:1256463", "name": "Minami, Sota", "country": "Japan", "country_code": "JPN", "abbreviation": "MIN", "qualifier": "home"},
                            {"id": "sr:competitor:686611", "name": "Walia, Drona", "country": "India", "country_code": "IND", "abbreviation": "WAL", "qualifier": "away"}
                        ],
                        "venue": {"id": "sr:venue:82203", "name": "Yang-Ming Tennis Center - Court 7", "city_name": "Kaohsiung", "country_name": "Chinese Taipei", "country_code": "TPE", "timezone": "Asia/Taipei"},
                        "estimated": False
                    },
                    "sport_event_status": {
                        "status": "live",
                        "match_status": "2nd_set",
                        "home_score": 1,
                        "away_score": 0,
                        "period_scores": [
                            {"home_score": 6, "away_score": 2, "type": "set", "number": 1},
                            {"home_score": 4, "away_score": 1, "type": "set", "number": 2}
                        ],
                        "game_state": {
                            "home_score": 0, "away_score": 0, "serving": "home", "last_point_result": "server_winner", "tie_break": False
                        }
                    },
                    "statistics": {
                        "totals": {
                            "competitors": [
                                {"id": "sr:competitor:1256463", "name": "Minami, Sota", "abbreviation": "MIN", "qualifier": "home", "statistics": {"aces": 1, "breakpoints_won": 6, "double_faults": 4, "first_serve_points_won": 15, "first_serve_successful": 25, "games_won": 10, "max_games_in_a_row": 6, "max_points_in_a_row": 6, "points_won": 57, "second_serve_points_won": 9, "second_serve_successful": 13, "service_games_won": 4, "service_points_lost": 18, "service_points_won": 24, "tiebreaks_won": 0, "total_breakpoints": 9}},
                                {"id": "sr:competitor:686611", "name": "Walia, Drona", "abbreviation": "WAL", "qualifier": "away", "statistics": {"aces": 2, "breakpoints_won": 2, "double_faults": 3, "first_serve_points_won": 14, "first_serve_successful": 33, "games_won": 3, "max_games_in_a_row": 1, "max_points_in_a_row": 4, "points_won": 39, "second_serve_points_won": 7, "second_serve_successful": 18, "service_games_won": 1, "service_points_lost": 33, "service_points_won": 21, "tiebreaks_won": 0, "total_breakpoints": 6}}
                            ]
                        }
                    }
                }
            ]
        }

    # Mock para la función H2H (ejemplo)
    def get_head_to_head_stats_mock(id1, id2):
        # Este mock asume una respuesta simple de la API H2H de Sportradar
        # ¡AJUSTA ESTO PARA QUE COINCIDA CON LO QUE REALMENTE DEVUELVE TU API H2H!
        return {
            "head_to_head": {
                "home_competitor_id": id1,
                "away_competitor_id": id2,
                "home_wins": 3,
                "away_wins": 1,
                "total_meetings": 4
            }
        }

    original_get_live_matches = get_live_matches
    original_get_head_to_head_stats = get_head_to_head_stats

    globals()['get_live_matches'] = get_live_matches_sportradar_mock
    globals()['get_head_to_head_stats'] = get_head_to_head_stats_mock 

    state = LiveMatchState()
    state.load_matches()

    if state.matches:
        print("\n✅ Datos del primer partido procesado de Sportradar (con H2H):")
        first_match_obj = state.matches[0]
        print(f"  Torneo: {first_match_obj.TOURNAMENT_NAME} ({first_match_obj.TOURNAMENT_YEAR})")
        print(f"  Partido: {first_match_obj.HOME_NAME} vs {first_match_obj.AWAY_NAME}")
        print(f"  Ronda: {first_match_obj.ROUND}")
        print(f"  Hora: {first_match_obj.FORMATTED_TIME}")
        print(f"  Estado: {first_match_obj.MATCH_STATUS} ({first_match_obj.STATUS_TYPE})")
        print(f"  País Local: {first_match_obj.HOME_COUNTRY}")
        print(f"  País Visitante: {first_match_obj.AWAY_COUNTRY}")
        print(f"  IDs: {first_match_obj.HOME_ID} vs {first_match_obj.AWAY_ID}")
        print(f"  Set actual: {first_match_obj.CURRENT_SET}, Score set: {first_match_obj.HOME_SCORE_CURRENT_SET}-{first_match_obj.AWAY_SCORE_CURRENT_SET}")
        print(f"  Puntos juego: {first_match_obj.GAME_STATE_HOME_SCORE}-{first_match_obj.GAME_STATE_AWAY_SCORE}, Sirve: {first_match_obj.SERVING_PLAYER}")
        print(f"  H2H: {first_match_obj.HEAD_TO_HEAD_WINS_HOME}-{first_match_obj.HEAD_TO_HEAD_WINS_AWAY} ({first_match_obj.HEAD_TO_HEAD_TOTAL_MATCHES} partidos)")
        print(f"  Porcentaje H2H Home: {first_match_obj.HOME_WIN_PERCENTAGE_H2H}%")
        print(f"  Porcentaje H2H Away: {first_match_obj.AWAY_WIN_PERCENTAGE_H2H}%")
    else:
        print("🚫 No se procesó ningún partido (después de intentar con Sportradar y H2H).")
    
    globals()['get_live_matches'] = original_get_live_matches
    globals()['get_head_to_head_stats'] = original_get_head_to_head_stats