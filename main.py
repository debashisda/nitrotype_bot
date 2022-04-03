import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

username = "nitrotype_bot_test3"
password = "http$3A%2F"
typing_speed = 1/(7.6) #almost around 75 - 80 WPM
chromedriver_path = r'C:/chromedriver.exe'

def clear_window():
    clear = lambda:os.system('cls')
    clear()
    
def prepare_browser():
    global driver
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    
def fetch_paragraph():
    driver.execute_script("a=[];e=document.getElementsByClassName('dash-letter');l=document.getElementsByClassName('dash-letter').length;for(let i=0;i<l;i++){a[i]=e[i].innerHTML;}")
    paragraph = driver.execute_script("return a;")
    paragraph = paragraph[:-1]
    return paragraph

def login_to_nitrotype():
    driver.get("https://www.nitrotype.com/login")
    driver.maximize_window()
    driver.find_element_by_id("username").send_keys(username)
    time.sleep(3)
    driver.find_element_by_id("password").send_keys(password)
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='root']/div/div/main/div/section/div[2]/div/div[3]/form/button").click()
    time.sleep(4)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        
def race_with_players():  
    wait = input("Press ENTER when the race starts! ")   
    paragraph = fetch_paragraph()
    for letter in paragraph:
        if letter == '&nbsp;':
            time.sleep(typing_speed)
            webdriver.ActionChains(driver).send_keys(Keys.SPACE).perform()
        else:
            time.sleep(typing_speed)
            webdriver.ActionChains(driver).send_keys(letter).perform()
    time.sleep(5)
    if driver.find_element_by_xpath("//*[@id='raceContainer']/div[1]/div[2]/div[4]/div/div[2]/button").is_displayed() == True:
        print("Race Finished...!")
        time.sleep(2)

def check_race_invites():
    count = driver.execute_script("return document.getElementsByClassName('growl').length;")
    if count >= 1:
        ch = input("Invite Found. Want to join?(Y/N): ")
        if ch == 'Y' or ch == 'y':
            link = driver.execute_script("return document.getElementsByTagName('a')[0].getAttribute('href');")
            return link
        elif ch == 'N' or ch == 'n':
            return -1
            #driver.find_element_by_xpath("//*[@id='root']/div[1]/div/button").click()
    else:
        return 0

def race_with_friend():    
    race_link = check_race_invites()
    if race_link != 0 or race_link !=-1:
        driver.get("https://nitrotype.com" + str(race_link))        
        race_with_players()
    elif race_link == -1:
        print("Ok! You don't want to race with your friend....")
        time.sleep(2)
    else:
        print("No Invitation Found...")
        time.sleep(1)    

def logout_and_exit():
    driver.execute_script("window.localStorage.clear();")
    driver.close()
    exit()    
    
def main():
    prepare_browser()
    login_to_nitrotype()    
    while(1):
        clear_window()        
        ch = int(input("1)Race With Random Players\n2)Check for Invites\n3)Go to Garage\n4)Logout & Exit\nOption: "))
        if ch == 1: 
            driver.get("https://nitrotype.com/race")
            race_with_players()          
        elif ch == 2:            
            race_with_friend()            
        elif ch == 3:
            driver.get("https://www.nitrotype.com/garage")
        elif ch == 4:
            logout_and_exit()            
        else:
            print("Enter Valid Input !!!")
            time.sleep(1)
      
if __name__ == "__main__":
    main()
