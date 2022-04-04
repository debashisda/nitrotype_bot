import selenium
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

def load_data():
    global data
    with open('data.json') as data_file:
        data = json.load(data_file)

def clear_window():
    clear = lambda:os.system('cls')
    clear()
    
def prepare_browser():
    global driver
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(executable_path=data['path'], options=options)

def login_to_nitrotype():
    driver.get("https://www.nitrotype.com/login")
    driver.maximize_window()
    driver.find_element_by_id("username").send_keys(data['username'])
    time.sleep(2)
    driver.find_element_by_id("password").send_keys(data['password'])
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='root']/div/div/main/div/section/div[2]/div/div[3]/form/button").click()
    time.sleep(3)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        
def race_with_players():
    #race_status = driver.execute_script("return document.getElementsByClassName('bucket-content').length;")
    #race_status = driver.execute_script("return document.getElementsByClassName('tsxxl mbf tlh-1')[0].innerHTML;")   
    wait = input("Press ENTER when the race starts! ")
    driver.execute_script("a=[];e=document.getElementsByClassName('dash-letter');l=document.getElementsByClassName('dash-letter').length;for(let i=0;i<l;i++){a[i]=e[i].innerHTML;}")
    paragraph = driver.execute_script("return a;")        
    paragraph = paragraph[:-1]
    for letter in paragraph:
        if letter == '&nbsp;':
            time.sleep(data['typing_speed'])
            webdriver.ActionChains(driver).send_keys(Keys.SPACE).perform()
        else:
            time.sleep(data['typing_speed'])
            webdriver.ActionChains(driver).send_keys(letter).perform()
    time.sleep(5)    
    if int(driver.execute_script("return Boolean(document.getElementsByClassName('raceResults-titles').length);")) == 1:
        print("Race Finished...!")        
        time.sleep(2)
    else:
        driver.get("https://www.nitrotype.com/garage")        

def check_race_invites():
    count = driver.execute_script("return document.getElementsByClassName('growl').length;")
    if count == 1:
        ch = input("Invite Found. Want to join?(Y/N): ")
        if ch == 'Y' or ch == 'y':
            link = driver.execute_script("return document.getElementsByTagName('a')[0].getAttribute('href');")
            return link
        elif ch == 'N' or ch == 'n':
            if count >= 1:
                driver.find_element_by_xpath("//*[@id='root']/div[1]/div/button").click()
            return 'N'
    else:
        return 0

def race_with_friend():    
    race_link = check_race_invites()
    if race_link != 0 and race_link !='N':
        driver.get("https://nitrotype.com" + str(race_link))        
        race_with_players()
    elif race_link == 'N':
        print("Never Mind....")
        time.sleep(2)
    else:
        print("No Invites Found...")
        time.sleep(1)    

def logout_and_exit():
    driver.execute_script("window.localStorage.clear();")
    driver.close()
    exit()    
    
def main():
    load_data()
    prepare_browser()
    login_to_nitrotype()    
    while(1):
        clear_window()
        print("1)Race With Random Players\n2)Check for Invites\n3)Go to Garage\n4)Logout & Exit\n")
        ch = int(input("Option: "))
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
