import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

username = "nitrotype_bot_test3"
password = "http$3A%2F"
typing_speed = 1/7 #almost around 75 - 80 WPM
chromedriver_path = r'C:/chromedriver.exe'

def prepare_browser():
    global driver
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    
def fetch_paragraph():
    driver.execute_script("a=[];e=document.getElementsByClassName('dash-letter');for(let i=0;i<(document.getElementsByClassName('dash-letter').length);i++){a[i]=e[i].innerHTML;}")
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

def check_race_invites():
    count = driver.execute_script("return document.getElementsByClassName('growl').length;")
    if count >= 1:
        ch = input("Invite Found. Want to join?(Y/N): ")
        if ch == 'Y' or ch == 'y':
            link = driver.execute_script("return document.getElementsByTagName('a')[0].getAttribute('href');")
            return link
        elif ch == 'N' or ch == 'n':
            driver.find_element_by_xpath("//*[@id='root']/div[1]/div/button").click()
    else:
        return 0;

def main():
    prepare_browser()
    login_to_nitrotype()    
    while(1):
        ch = int(input("1)Race With Random Players\n2)Check for Invites\n3)Exit\nOption: "))
        if ch == 1: 
            driver.get("https://nitrotype.com/race")
            race_with_players()          
        elif ch == 2:    
            race_link = check_race_invites()
            if race_link != 0:                
                driver.get("https://nitrotype.com" + str(race_link))
                driver.find_element_by_xpath("//*[@id='root']/div[1]/div/button").click()
                race_with_players()
            else:
                print("No Invitation Found...")
        elif ch == 3:
            exit()
        else:
            print("Enter Valid Input !!!")           
      
if __name__ == "__main__":
    main()
