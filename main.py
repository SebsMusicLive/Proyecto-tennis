
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def main():
    
    
#preparacion del web scrapping
    opts= Options()
    opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36')
    driver=webdriver.Chrome(service= Service(ChromeDriverManager().install()),options=opts)

#direccionando pagina
    driver.get("https://www.atptour.com/es/stats/leaderboard?boardType=serve&timeFrame=52week&surface=all&versusRank=all&formerNo1=false")
    sleep(5)

#Listas

posicionList =[]
jugadorList =[]
efecSaqueList =[]
porcPrimerSaqueList =[]
porcSegundoSaqueList =[]
porcJuegosGanadosSaqueList =[]
promedioAcesPartidoList =[]
promDoblesList =[]


#Recolectando informacion de columnas

    col1 = driver.find_elements(By.XPATH,'//tbody/tr/td[1]')
    col2 = driver.find_elements(By.XPATH,'//tbody/tr/td[2]')
    col3 = driver.find_elements(By.XPATH,'//tbody/tr/td[3]')
    col4 = driver.find_elements(By.XPATH,'//tbody/tr/td[4]')
    col5 = driver.find_elements(By.XPATH,'//tbody/tr/td[5]')
    col6 = driver.find_elements(By.XPATH,'//tbody/tr/td[6]')
    col7 = driver.find_elements(By.XPATH,'//tbody/tr/td[7]')
    col8 = driver.find_elements(By.XPATH,'//tbody/tr/td[8]')
    col9 = driver.find_elements(By.XPATH,'//tbody/tr/td[9]')
    


  #proceso llenado listas  

    for c1 in col1:

        try:
            info1= c1.text
            posicionList.append(info1)

        except Exception as e:
            
            info1 =''
    
    for c2 in col2:

        try:
            info2= c2.text
            jugadorList.append(info2)

        except Exception as e:
            
            info2 =''

    for c3 in col3:

        try:
            info3= c3.text
            efecSaqueList.append(info3)

        except Exception as e:
            
            info3 =''

    for c4 in col4:

        try:
            info4= c4.text
            porcPrimerSaqueList.append(info4)

        except Exception as e:
            
            info4 =''

    for c5 in col5:

        try:
            info5= c5.text
            porcSegundoSaqueList.append(info5)

        except Exception as e:
            
            info5 =''

    for c6 in col6:

        try:
            info6= c6.text
            porcJuegosGanadosSaqueList.append(info6)

        except Exception as e:
            
            info6 =''

    for c17in col7:

        try:
            info7= c7.text
            promedioAcesPartidoList.append(info7)

        except Exception as e:
            
            info7 =''


    for c8 in col8:

        try:
            info8= c8.text
            promDoblesList.append(info8)

        except Exception as e:
            
            info8 =''



    driver.quit()





if __name__ =="__main__":
    main()