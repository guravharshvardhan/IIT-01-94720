from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


options = Options()

options.add_argument("--user-data-dir=C:/temp/selenium-profile")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://sunbeaminfo.in/")
print("Page title:", driver.title)

wait = WebDriverWait(driver, 15)

#internship button
internship_button=wait.until(
    EC.presence_of_element_located((By.XPATH,"//a[@href='collapseSix']//Internship"))
)
driver.execute_script("argument[0].click();",internship_button)
# Scroll down
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

# Click "Available Internship Programs"
plus_button = wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[@href='#collapseSix']"))
)
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", plus_button)
time.sleep(1)
driver.execute_script("arguments[0].click();", plus_button)

# Wait for table to load
table = wait.until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='collapseSix']//table"))
)

rows = table.find_elements(By.XPATH, ".//tbody/tr")

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 5:
        info = {
            "Technology": cols[0].text,
            "Aim": cols[1].text,
            "Prerequisite": cols[2].text,
            "Learning": cols[3].text,
            "Location": cols[4].text
        }
        print(info)

driver.quit()