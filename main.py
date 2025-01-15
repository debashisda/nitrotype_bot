import time
import os
import json
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import pyfiglet
from pyfiglet import Figlet

def load_signature():
    custom_fig = Figlet(font='graffiti')
    print(custom_fig.renderText('NitroType'))
    print("\t\t\t~ Debashis Das ~")

def load_data():
    global data
    with open('data.json') as data_file:
        data = json.load(data_file)

def clear_console():
    clear = lambda:os.system('cls')
    clear()

#OLD Code
#def load_driver():
#    global driver
#    options = Options()
#    service = service()
#    options.add_experimental_option("excludeSwitches",["enable-logging"])
#    driver = webdriver.Chrome(service=service,options=options)

def load_driver():
    global driver
    chrome_options = Options()
    service = Service()
    os.system("start chrome.exe --remote-debugging-port=9222")
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(service=service, options=chrome_options)

def login_to_nitrotype():    
    driver.execute_script("window.open('https://nitrotype.com/login','_self');")    
    driver.maximize_window()
    driver.find_element("id","username").send_keys(data['username'])       
    driver.find_element("id","password").send_keys(data['password'])
    # time.sleep(2) # enable if the captcha is getting triggered
    driver.find_element("xpath","//*[@id='root']/div/div/main/div/section/div[2]/div/div[3]/form/button").click()
    '''modal = driver.execute_script("return document.getElementsByClassName('modal is-active modal--a modal--l').length;")
    if modal == 1:
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    else:
        time.sleep(5)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()'''
    time.sleep(2)
    driver.execute_script("window.open('https://nitrotype.com/garage','_self');")
            
def race_with_players():
    driver.execute_script("a=[];")
    wait = input("Press ENTER when the race starts! ")
    # needs Optimization and find a better way to execute the below JS    
    driver.execute_script("e=document.getElementsByClassName('dash-letter');for(let i=0;i<e.length;i++){a[i]=e[i].innerHTML;}")
    paragraph = driver.execute_script("return a;")   
    for letter in paragraph:
        if letter == '&nbsp;':
            webdriver.ActionChains(driver).send_keys(Keys.SPACE).perform()            
        else:
            webdriver.ActionChains(driver).send_keys(letter).perform()
        time.sleep(data['typing_speed'])
    time.sleep(5)
    if int(driver.execute_script("return Boolean(document.getElementsByClassName('raceResults-titles').length);")) == 1:
        time.sleep(2)
    else:
        print("Something went wrong...!!!")
        time.sleep(2)
        driver.execute_script("window.open('https://nitrotype.com/garage','_self');")  

def check_race_invites():
    count = driver.execute_script("return document.getElementsByClassName('growl').length;")
    if count == 1:
        ch = input("Invite Found. Want to join?(Y/N): ")
        if ch == 'Y' or ch == 'y':
            link = driver.execute_script("return document.getElementsByTagName('a')[0].getAttribute('href');")            
            driver.find_element("xpath","//*[@id='root']/div[1]/div/button").click()
            return link
        elif ch == 'N' or ch == 'n':
            if count >= 1:                
                driver.find_element("xpath","//*[@id='root']/div[1]/div/button").click()
                return 'N'
    else:
        return 0

def race_with_friends():
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
    sure = str(input("Are you sure?(Y/N): "))
    if sure == 'Y' or sure == 'y':
        #driver.execute_script("window.localStorage.clear();")
        #driver.close()
        os._exit(0)
    else:
        return
    
def main():
    load_data()
    load_driver()
    clear_console()
    login_to_nitrotype()
    while(1):
        ch = 0
        clear_console()
        load_signature()
        print("1)Join Race With Random Players \n2)Join Race With Invites \n3)Go to Garage \n4)Logout & Exit \n")
        ch = int(input("Option:"))
        if ch == 1:           
            driver.execute_script("window.open('https://nitrotype.com/race','_self');")
            race_with_players()
        elif ch == 2:
            race_with_friends()
        elif ch == 3:
            driver.execute_script("window.open('https://nitrotype.com/garage','_self');")            
        elif ch == 4:
            break
        else:
            print("Please Enter a Valid Input !!!")
            time.sleep(1)
    print("Logging out...")
    logout_and_exit()
            
if __name__ == "__main__":
    main()    
