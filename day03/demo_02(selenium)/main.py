from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
#start the selenium browser session

driver =webdriver.Chrome()
#load desired pagein browser

driver.get("https://duckduckgo.com/")
#print("Initial page title:",driver.title)
driver.implicitly_wait(5)

#now access the controlon the page

search_box = driver.find_element(By.NAME,"q")

search_box.send_keys("dkte collage of engineering ichalkaranji")
search_box.send_keys(Keys.RETURN)
#wait for the result
print("later page title:", driver.title)

#stopthe session
time.sleep(10)
driver.quit