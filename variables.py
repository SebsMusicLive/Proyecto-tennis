from datetime import datetime

ruta = 'https://www.atptour.com/es/stats/leaderboard?boardType=serve&timeFrame=52week&surface=all&versusRank=all&formerNo1=false'

fecha_actual = datetime.now().strftime('%Y-%m-%d')
nombre_archivo = 'jugadores_'
extension = '.xlsx'
nombre_completo = nombre_archivo + fecha_actual + extension

# print(nombre_completo)