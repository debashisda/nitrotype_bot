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
    driver.execute_script("window.open('https://nitrotype.com/login','_self');")    
    driver.maximize_window()
    driver.find_element_by_id("username").send_keys(data['username'])    
    driver.find_element_by_id("password").send_keys(data['password'])
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='root']/div/div/main/div/section/div[2]/div/div[3]/form/button").click()
    time.sleep(3)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        
def race_with_players():
    driver.execute_script("a=[];")
    wait = input("Press ENTER when the race starts! ")
    # needs Optimization and find better way to execute the below JS    
    driver.execute_script("e=document.getElementsByClassName('dash-letter');l=e.length;for(let i=0;i<l;i++){a[i]=e[i].innerHTML;}")
    paragraph = driver.execute_script("return a;")   
    for letter in paragraph:
        if letter == '&nbsp;':
            webdriver.ActionChains(driver).send_keys(Keys.SPACE).perform()
            time.sleep(data['typing_speed'])
        else:
            webdriver.ActionChains(driver).send_keys(letter).perform()
            time.sleep(data['typing_speed'])
    time.sleep(5)
    if int(driver.execute_script("return Boolean(document.getElementsByClassName('raceResults-titles').length);")) == 1:
        print("Race is Finished...!")
        time.sleep(2)
    else:
        print("Script malfunctioning...")
        time.sleep(2)
        driver.execute_script("window.open('https://nitrotype.com/garage','_self');")  

def check_race_invites():
    count = driver.execute_script("return document.getElementsByClassName('growl').length;")
    if count == 1:
        ch = input("Invite Found. Want to join?(Y/N): ")
        if ch == 'Y' or ch == 'y':
            link = driver.execute_script("return document.getElementsByTagName('a')[0].getAttribute('href');")
            return link
        elif ch == 'N' or ch == 'n':
            if count >= 1:
                # this button click creates error sometimes
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
        # main function creates error sometimes
        print("1)Race With Random Players\n2)Check for Invites\n3)Go to Garage\n4)Logout & Exit\n")
        ch = int(input("Option: "))
        if ch == 1:           
            driver.execute_script("window.open('https://nitrotype.com/race','_self');")
            race_with_players()
        elif ch == 2:
            race_with_friend()
        elif ch == 3:
            driver.execute_script("window.open('https://nitrotype.com/garage','_self');")            
        elif ch == 4:
            logout_and_exit()
        else:
            print("Please Enter a Valid Input !!!")
            time.sleep(1)
            
if __name__ == "__main__":
    main()
    
