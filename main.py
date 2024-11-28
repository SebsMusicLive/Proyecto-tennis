from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service

def main():
    
    
    service=Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    option.add_argument("--window-size=1920,1080")
    driver= Chrome(service=service,option=option)
    driver.get("https://www.atptour.com/es/stats/leaderboard?boardType=serve&timeFrame=52week&surface=all&versusRank=all&formerNo1=false")
    
    



    driver.quit()





if __name__ =="__main__":
    main()