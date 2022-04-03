import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

#typing_speed = 5/25 # 56 wpm
typing_speed = 1/10 #76
 
driver = webdriver.Chrome(executable_path=r"C:/chromedriver.exe")
driver.get("https://www.nitrotype.com/race")
driver.maximize_window()
wait = input("Press ENTER to start race ")
driver.execute_script("a=[];e=document.getElementsByClassName('dash-letter');for(let i=0;i<(document.getElementsByClassName('dash-letter').length);i++){a[i]=e[i].innerHTML;}")
text = driver.execute_script("return a;")
text = text[:-1]
print(text)
for i in text:
  if i == '&nbsp;':
    time.sleep(typing_speed)
    webdriver.ActionChains(driver).send_keys(Keys.SPACE).perform()
  else:
    time.sleep(typing_speed)
    webdriver.ActionChains(driver).send_keys(i).perform()
