from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from variables import * 
from time import sleep

import pandas as pd

#Preparación del WebScraping
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = opts)

driver.get(ruta)
sleep(8)

#Listas
id_list = []
jugador_list = []
efectividad_list = []
primer_saque_list = []
puntos_primer_list = []
puntos_segundo_list = []
juegos_saque_list = []

#Columnas
id_columna_1 = driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
jugador_columna_2 = driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
efectividad_columna_3 = driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
primer_saque_columna_4 = driver.find_elements(By.XPATH, '//tbody/tr/td[4]')
puntos_primer_columna_5 = driver.find_elements(By.XPATH, '//tbody/tr/td[5]')
puntos_segundo_columna_6 = driver.find_elements(By.XPATH, '//tbody/tr/td[6]')
juegos_saque_columna_7 = driver.find_elements(By.XPATH, '//tbody/tr/td[7]')

for c1 in id_columna_1:
    try: 
        id = c1.text
        #id = id.split("\n")

        id_list.append(id)
        id_list = id_list(filter(lambda x:x != "", id_list))

        # print(id)
    except Exception as e:
        print(e)

# print(id_list)

for c2 in jugador_columna_2:
    try: 
        jugador = c2.text
        #jugador = jugador.split("\n")

        jugador_list.append(jugador)

        #print(jugador)
    except Exception as e:
        print(e)

for c3 in efectividad_columna_3:
    try: 
        efectividad = c3.text
        #efectividad = efectividad.split("\n")
        
        efectividad_list.append(efectividad)
        
        #print(efectividad)
    except Exception as e:
        print(e)

for c4 in primer_saque_columna_4:
    try:
        primer_saque = c4.text
        #primer_saque = primer_saque.split("\n")
        
        primer_saque_list.append(primer_saque)
        
        #print(primer_saque)
    except Exception as e:
        print(e)

for c5 in puntos_primer_columna_5:
    try:
        puntos_primer = c5.text
        #puntos_primer = puntos_primer.split('\n')
        
        puntos_primer_list.append(puntos_primer)
        
        #print(puntos_primer)
    except Exception as e:
        print(e)

for c6 in puntos_segundo_columna_6:
    try:
        puntos_segundo = c6.text
        #puntos_segundo = puntos_segundo.split('\n')
        
        puntos_segundo_list.append(puntos_segundo)

        #print(puntos_segundo)
    except Exception as e:
        print(e)

for c7 in juegos_saque_columna_7:
    try:
        juegos_saque = c7.text
        #juegos_saque = juegos_saque.split('\n')
        
        juegos_saque_list.append(juegos_saque)
        
        #print(juegos_saque)
    except Exception as e:
        print(e)

df = pd.DataFrame({
    'id':id_list,
    'jugador':jugador_list,
    'efectividad':efectividad_list,
    'primer_saque':primer_saque_list,
    'puntos_primer':puntos_primer_list,
    'puntos_segundo':puntos_segundo_list,
    'juegos_saque':juegos_saque_list
})

print(df)

df.to_excel(nombre_completo, index = False)