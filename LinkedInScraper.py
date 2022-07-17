from selenium import webdriver as wd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as expections
from selenium.webdriver.chrome.options import Options
import time


linkedin_username = 'Enter Linkedin Username'
linkedin_password = 'Enter Linkedin Password'

message = "Enter Custom note"
search = "Search Query"
pages = 2
driver_path = r'Enter Chrome driver path'

query = search.replace(" ","%20")

options = wd.ChromeOptions()
# options.add_argument("Start-maximized")
# options.add_experimental_option("excludeSwitches",["enable-automation"])
options.add_experimental_option("detach", True)

#need to create a login session to maintain login during diff 

driver = wd.Chrome(options=options, executable_path=driver_path)

try:  
    driver.get('https://www.linkedin.com/login')
    time.sleep(3)
    WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(linkedin_username)
    #username_field = driver.find_element("xpath", "//input[@name='session_key']")
    #username_field.send_keys(linkedin_username)
    password_field = driver.find_element("xpath", "//input[@name='session_password']")
    password_field.send_keys(linkedin_password);

    driver.find_element("xpath" ,'//button[@type="submit"]').click()
    time.sleep(2)
    for i in range(1,pages,1):
        driver.get(f'https://www.linkedin.com/search/results/people/?keywords={query}&page={i}')
        time.sleep(2)
        allButtons = driver.find_elements(By.TAG_NAME, "button")
        connectButtons = [btn for btn in allButtons if btn.text=="Connect"]
        for member in connectButtons:
            driver.execute_script("arguments[0].click();", member)
            time.sleep(1)
            allButtons = driver.find_elements(By.TAG_NAME, "button")
            [note] = [btn for btn in allButtons if btn.text=="Add a note"]
            driver.execute_script("arguments[0].click();", note)
            time.sleep(1)
            driver.find_element(By.TAG_NAME, "textarea").send_keys(message)
            time.sleep(1)
            allButtons = driver.find_elements(By.TAG_NAME, "button")
            [send] = [btn for btn in allButtons if btn.text=="Send"]
            driver.execute_script("arguments[0].click();", send)
            time.sleep(2)

except Exception as e:
    print(e)
    driver.quit()
