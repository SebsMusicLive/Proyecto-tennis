# backend/live_state.py

import reflex as rx
import datetime
import json
from ..backend.api_client import get_live_matches # Solo necesitamos get_live_matches ahora

# Modelo para representar un partido en vivo
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
    
    HOME_ACES: int = 0
    AWAY_ACES: int = 0
    HOME_BREAKPOINTS_WON: int = 0
    AWAY_BREAKPOINTS_WON: int = 0
    HOME_DOUBLE_FAULTS: int = 0
    AWAY_DOUBLE_FAULTS: int = 0
    HOME_FIRST_SERVE_SUCCESSFUL: int = 0
    AWAY_FIRST_SERVE_SUCCESSFUL: int = 0
    HOME_SERVICE_POINTS_WON: int = 0 
    AWAY_SERVICE_POINTS_WON: int = 0

    # 🚨 NUEVOS CAMPOS PARA PORCENTAJES BASADOS EN ESTADÍSTICAS DEL PARTIDO ACTUAL
    HOME_FIRST_SERVE_WIN_PERCENTAGE: str = "0.0%" # % de puntos ganados con el 1er saque
    AWAY_FIRST_SERVE_WIN_PERCENTAGE: str = "0.0%"

    HOME_SERVICE_POINTS_WIN_PERCENTAGE: str = "0.0%" # % de puntos de servicio ganados (total)
    AWAY_SERVICE_POINTS_WIN_PERCENTAGE: str = "0.0%"

    HOME_BREAKPOINT_CONVERSION_PERCENTAGE: str = "0.0%" # % de puntos de quiebre convertidos
    AWAY_BREAKPOINT_CONVERSION_PERCENTAGE: str = "0.0%"


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

        try:
            for match_summary in raw_matches: 
                sport_event = match_summary.get("sport_event", {})
                sport_event_status = match_summary.get("sport_event_status", {})
                sport_event_context = sport_event.get("sport_event_context", {}) 
                statistics = match_summary.get("statistics", {}).get("totals", {}).get("competitors", []) 

                competitors = sport_event.get("competitors", []) 
                
                home_data = next((c for c in competitors if c.get("qualifier") == "home"), {})
                away_data = next((c for c in competitors if c.get("qualifier") == "away"), {})

                home_name = home_data.get("name", "Desconocido")
                away_name = away_data.get("name", "Desconocido")
                
                home_country = home_data.get("country", "")
                away_country = away_data.get("country", "")

                home_id = home_data.get("id", "")
                away_id = away_data.get("id", "")

                home_stats = next((s.get("statistics", {}) for s in statistics if s.get("id") == home_id), {})
                away_stats = next((s.get("statistics", {}) for s in statistics if s.get("id") == away_id), {})

                home_aces = home_stats.get("aces", 0)
                away_aces = away_stats.get("aces", 0)
                home_breakpoints_won = home_stats.get("breakpoints_won", 0)
                away_breakpoints_won = away_stats.get("breakpoints_won", 0)
                home_double_faults = home_stats.get("double_faults", 0)
                away_double_faults = away_stats.get("double_faults", 0)
                home_first_serve_successful = home_stats.get("first_serve_successful", 0)
                away_first_serve_successful = away_stats.get("first_serve_successful", 0)
                home_service_points_won = home_stats.get("service_points_won", 0)
                away_service_points_won = away_stats.get("service_points_won", 0)
                
                # Necesitamos los puntos de primer saque ganados y los totales para el %
                home_first_serve_points_won = home_stats.get("first_serve_points_won", 0)
                away_first_serve_points_won = away_stats.get("first_serve_points_won", 0)

                # Necesitamos los puntos de servicio perdidos para el % de puntos de servicio ganados
                home_service_points_lost = home_stats.get("service_points_lost", 0)
                away_service_points_lost = away_stats.get("service_points_lost", 0)

                # Necesitamos los breakpoints totales para el % de quiebres convertidos
                home_total_breakpoints = home_stats.get("total_breakpoints", 0)
                away_total_breakpoints = away_stats.get("total_breakpoints", 0)


                round_data = sport_event_context.get("round", {})
                round_name = round_data.get("name", "Sin ronda") if isinstance(round_data, dict) else str(round_data)
                if not round_name and "number" in round_data: 
                    round_name = f"Ronda {round_data['number']}"


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

                # 🚨 ELIMINAMOS LA LÓGICA H2H YA QUE NO TENEMOS ACCESO DIRECTO
                # Y NOS ENFOCAMOS EN LOS PORCENTAJES DEL PARTIDO ACTUAL
                home_win_percentage_h2h_str = "N/A" # Lo mantenemos como N/A o lo eliminamos si no se va a usar
                away_win_percentage_h2h_str = "N/A" # Lo mantenemos como N/A o lo eliminamos si no se va a usar

                # --- CÁLCULO DE LOS PORCENTAJES DEL PARTIDO ACTUAL ---
                home_first_serve_win_pct = "0.0%"
                if home_first_serve_successful > 0:
                    home_first_serve_win_pct = f"{(home_first_serve_points_won / home_first_serve_successful * 100):.1f}%"

                away_first_serve_win_pct = "0.0%"
                if away_first_serve_successful > 0:
                    away_first_serve_win_pct = f"{(away_first_serve_points_won / away_first_serve_successful * 100):.1f}%"


                home_service_points_win_pct = "0.0%"
                total_home_service_points = home_service_points_won + home_service_points_lost
                if total_home_service_points > 0:
                    home_service_points_win_pct = f"{(home_service_points_won / total_home_service_points * 100):.1f}%"
                
                away_service_points_win_pct = "0.0%"
                total_away_service_points = away_service_points_won + away_service_points_lost
                if total_away_service_points > 0:
                    away_service_points_win_pct = f"{(away_service_points_won / total_away_service_points * 100):.1f}%"


                home_breakpoint_conversion_pct = "0.0%"
                if home_total_breakpoints > 0:
                    home_breakpoint_conversion_pct = f"{(home_breakpoints_won / home_total_breakpoints * 100):.1f}%"
                
                away_breakpoint_conversion_pct = "0.0%"
                if away_total_breakpoints > 0:
                    away_breakpoint_conversion_pct = f"{(away_breakpoints_won / away_total_breakpoints * 100):.1f}%"

                # ----------------------------------------------------

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
                        # Campos H2H ahora pueden ser siempre "N/A" si no hay API H2H
                        HEAD_TO_HEAD_WINS_HOME=0, 
                        HEAD_TO_HEAD_WINS_AWAY=0,
                        HEAD_TO_HEAD_TOTAL_MATCHES=0,
                        HOME_WIN_PERCENTAGE_H2H=home_win_percentage_h2h_str, # Será N/A
                        AWAY_WIN_PERCENTAGE_H2H=away_win_percentage_h2h_str, # Será N/A
                        
                        HOME_ACES=home_aces,
                        AWAY_ACES=away_aces,
                        HOME_BREAKPOINTS_WON=home_breakpoints_won,
                        AWAY_BREAKPOINTS_WON=away_breakpoints_won,
                        HOME_DOUBLE_FAULTS=home_double_faults,
                        AWAY_DOUBLE_FAULTS=away_double_faults,
                        HOME_FIRST_SERVE_SUCCESSFUL=home_first_serve_successful,
                        AWAY_FIRST_SERVE_SUCCESSFUL=away_first_serve_successful,
                        HOME_SERVICE_POINTS_WON=home_service_points_won,
                        AWAY_SERVICE_POINTS_WON=away_service_points_won,

                        # Asignar los nuevos porcentajes calculados
                        HOME_FIRST_SERVE_WIN_PERCENTAGE=home_first_serve_win_pct,
                        AWAY_FIRST_SERVE_WIN_PERCENTAGE=away_first_serve_win_pct,
                        HOME_SERVICE_POINTS_WIN_PERCENTAGE=home_service_points_win_pct,
                        AWAY_SERVICE_POINTS_WIN_PERCENTAGE=away_service_points_win_pct,
                        HOME_BREAKPOINT_CONVERSION_PERCENTAGE=home_breakpoint_conversion_pct,
                        AWAY_BREAKPOINT_CONVERSION_PERCENTAGE=away_breakpoint_conversion_pct
                    )
                )
        except Exception as e:
            print(f"❌ Error al procesar un resumen del partido de Sportradar: {e}")
            
        self.matches = parsed_matches

# --- Bloque de Prueba (solo para ejecutar live_state.py directamente y probar) ---
# Si usas este bloque, asegúrate de que api_client.py no intente importar get_head_to_head_stats
# ya que lo hemos quitado. O ajusta los mocks para solo usar get_live_matches.
if __name__ == "__main__":
    # Mock para get_live_matches (ejemplo de respuesta de Sportradar summaries.json)
    def get_live_matches_sportradar_mock():
        return {
          "generated_at": "2025-06-16T01:58:58+00:00",
          "summaries": [
            {
              "sport_event": {
                "id": "sr:sport_event:61176665",
                "start_time": "2025-06-16T01:00:00+00:00",
                "start_time_confirmed": True,
                "sport_event_context": {
                  "sport": {"id": "sr:sport:5", "name": "Tennis"},
                  "category": {"id": "sr:category:2516", "name": "UTR Men"},
                  "competition": {"id": "sr:competition:47289", "name": "UTR PTT Fukui Men 01", "type": "singles", "gender": "men"},
                  "season": {"id": "sr:season:131225", "name": "2025 Fukui Men 01", "start_date": "2025-06-16", "end_date": "2025-06-22", "year": "2025", "competition_id": "sr:competition:47289"},
                  "stage": {"order": 1, "type": "league", "phase": "regular season", "start_date": "2025-06-16", "end_date": "2025-06-20", "year": "2025"},
                  "round": {"number": 1},
                  "groups": [{"id": "sr:league:94649", "name": "2025 Fukui Men 01, Group A", "group_name": "Group A"}],
                  "mode": {"best_of": 3}
                },
                "coverage": {
                  "type": "sport_event",
                  "sport_event_properties": {"enhanced_stats": False, "scores": "live", "detailed_serve_outcomes": True, "play_by_play": True}
                },
                "competitors": [
                  {"id": "sr:competitor:1213955", "name": "Wakamatsu, Taichi", "country": "Japan", "country_code": "JPN", "abbreviation": "WAK", "qualifier": "home"},
                  {"id": "sr:competitor:976405", "name": "Taguchi, Ryotaro", "country": "Japan", "country_code": "JPN", "abbreviation": "TAG", "qualifier": "away"}
                ],
                "venue": {"id": "sr:venue:83035", "name": "Fukui Sports Park - Court 2", "city_name": "Fukui", "country_name": "Japan", "country_code": "JPN", "timezone": "Asia/Tokyo"},
                "estimated": False
              },
              "sport_event_status": {
                "status": "live",
                "match_status": "1st_set",
                "home_score": 0,
                "away_score": 0,
                "period_scores": [
                  {"home_score": 3, "away_score": 5, "type": "set", "number": 1}
                ],
                "game_state": {
                  "home_score": 30, "away_score": 40, "serving": "home", "last_point_result": "receiver_winner", "tie_break": False, "point_type": "set"
                }
              },
              "statistics": {
                "totals": {
                  "competitors": [
                    {
                      "id": "sr:competitor:1213955", "name": "Wakamatsu, Taichi", "abbreviation": "WAK", "qualifier": "home",
                      "statistics": {
                        "aces": 2, "breakpoints_won": 1, "double_faults": 3, "first_serve_points_won": 10, "first_serve_successful": 14, "games_won": 3, "max_games_in_a_row": 1, "max_points_in_a_row": 3, "points_won": 20, "second_serve_points_won": 2, "second_serve_successful": 9, "service_games_won": 2, "service_points_lost": 14, "service_points_won": 12, "tiebreaks_won": 0, "total_breakpoints": 4
                      }
                    },
                    {
                      "id": "sr:competitor:976405", "name": "Taguchi, Ryotaro", "abbreviation": "TAG", "qualifier": "away",
                      "statistics": {
                        "aces": 2, "breakpoints_won": 2, "double_faults": 1, "first_serve_points_won": 15, "first_serve_successful": 18, "games_won": 5, "max_games_in_a_row": 4, "max_points_in_a_row": 9, "points_won": 30, "second_serve_points_won": 7, "second_serve_successful": 5, "service_games_won": 3, "service_points_lost": 8, "service_points_won": 16, "tiebreaks_won": 0, "total_breakpoints": 4
                      }
                    }
                  ]
                }
              }
            }
          ]
        }

    # Deshabilitamos el mock para get_head_to_head_stats ya que no lo usaremos directamente
    # def get_head_to_head_stats_mock(id1, id2):
    #     return {"head_to_head": {"home_wins": 0, "away_wins": 0, "total_meetings": 0}}

    original_get_live_matches = get_live_matches
    # original_get_head_to_head_stats = get_head_to_head_stats # No se necesita si lo hemos quitado

    globals()['get_live_matches'] = get_live_matches_sportradar_mock
    # globals()['get_head_to_head_stats'] = get_head_to_head_stats_mock 

    state = LiveMatchState()
    state.load_matches()

    if state.matches:
        print("\n✅ Datos del primer partido procesado de Sportradar (con estadísticas de partido):")
        first_match_obj = state.matches[0]
        print(f"  Torneo: {first_match_obj.TOURNAMENT_NAME} ({first_match_obj.TOURNAMENT_YEAR})")
        print(f"  Partido: {first_match_obj.HOME_NAME} vs {first_match_obj.AWAY_NAME}")
        print(f"  Ronda: {first_match_obj.ROUND}")
        print(f"  Hora: {first_match_obj.FORMATTED_TIME}")
        print(f"  Estado: {first_match_obj.MATCH_STATUS} ({first_match_obj.STATUS_TYPE})")
        print(f"  País Local: {first_match_obj.HOME_COUNTRY}")
        print(f"  País Visitante: {first_match_obj.AWAY_COUNTRY}")
        print(f"  IDs: {first_match_obj.HOME_ID} vs {first_match_obj.AWAY_ID}")
        print(f"  Set actual: {first_match_obj.CURRENT_SET}, Sets: {first_match_obj.HOME_SCORE_CURRENT_SET}-{first_match_obj.AWAY_SCORE_CURRENT_SET}")
        print(f"  Puntos juego: {first_match_obj.GAME_STATE_HOME_SCORE}-{first_match_obj.GAME_STATE_AWAY_SCORE}, Sirve: {first_match_obj.SERVING_PLAYER}")
        print(f"  Porcentaje 1er Saque Ganado Home: {first_match_obj.HOME_FIRST_SERVE_WIN_PERCENTAGE}")
        print(f"  Porcentaje 1er Saque Ganado Away: {first_match_obj.AWAY_FIRST_SERVE_WIN_PERCENTAGE}")
        print(f"  Porcentaje Puntos Servicio Ganados Home: {first_match_obj.HOME_SERVICE_POINTS_WIN_PERCENTAGE}")
        print(f"  Porcentaje Puntos Servicio Ganados Away: {first_match_obj.AWAY_SERVICE_POINTS_WIN_PERCENTAGE}")
        print(f"  Porcentaje Quiebres Convertidos Home: {first_match_obj.HOME_BREAKPOINT_CONVERSION_PERCENTAGE}")
        print(f"  Porcentaje Quiebres Convertidos Away: {first_match_obj.AWAY_BREAKPOINT_CONVERSION_PERCENTAGE}")
        print(f"  Aces: {first_match_obj.HOME_ACES}-{first_match_obj.AWAY_ACES}")
        print(f"  Breakpoints Ganados: {first_match_obj.HOME_BREAKPOINTS_WON}-{first_match_obj.AWAY_BREAKPOINTS_WON}")
        print(f"  Dobles Faltas: {first_match_obj.HOME_DOUBLE_FAULTS}-{first_match_obj.AWAY_DOUBLE_FAULTS}")
        print(f"  Primer Saque Exitoso: {first_match_obj.HOME_FIRST_SERVE_SUCCESSFUL}-{first_match_obj.AWAY_FIRST_SERVE_SUCCESSFUL}")
        print(f"  Puntos de Servicio Ganados: {first_match_obj.HOME_SERVICE_POINTS_WON}-{first_match_obj.AWAY_SERVICE_POINTS_WON}")

    else:
        print("🚫 No se procesó ningún partido.")
    
    globals()['get_live_matches'] = original_get_live_matches
    # if 'original_get_head_to_head_stats' in locals(): # Restaura si existía
    #     globals()['get_head_to_head_stats'] = original_get_head_to_head_stats