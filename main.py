import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

username = "icosidodecahedron"
password = "http$3A%2F"
typing_speed = 1/30

def prepare_browser():
    global driver
    options = Options()
    options.add_experimental_option("excludeSwitches",["enable-logging"])
    driver = webdriver.Chrome(executable_path=r'C:/chromedriver.exe', options=options)

def race_with_random_players():
    driver.get("https://nitrotype.com/race")
    wait = input("Press ENTER when the race starts! ")
    driver.execute_script("a=[];e=document.getElementsByClassName('dash-letter');for(let i=0;i<(document.getElementsByClassName('dash-letter').length);i++){a[i]=e[i].innerHTML;}")
    paragraph = driver.execute_script("return a;")
    paragraph = paragraph[:-1]    
    for i in paragraph:
        if i == '&nbsp;':
            time.sleep(typing_speed)
            webdriver.ActionChains(driver).send_keys(Keys.SPACE).perform()
        else:
            time.sleep(typing_speed)
            webdriver.ActionChains(driver).send_keys(i).perform()
    time.sleep(10)
    if driver.find_element_by_xpath("//*[@id='raceContainer']/div[1]/div[2]/div[4]/div/div[2]/button").is_displayed() == True:
        webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
    
def main():
    prepare_browser()   
    driver.get("https://www.nitrotype.com/login")
    driver.maximize_window()
    driver.find_element_by_id("username").send_keys(username)
    time.sleep(3)
    driver.find_element_by_id("password").send_keys(password)
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='root']/div/div/main/div/section/div[2]/div/div[3]/form/button").click()
    time.sleep(4)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    while(1):        
        ch = input("Want to race again?(Y/N): ")
        if ch == 'Y' or ch == 'y':            
            race_with_random_players()          
        else:
            exit()
      
if __name__ == "__main__":
    main()
