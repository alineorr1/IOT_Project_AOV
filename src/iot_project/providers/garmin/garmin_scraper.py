# Libraries
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import logging

#Logging config
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

#%%

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("start-maximized")
# options.add_argument("--headless")  
# options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED on Linux if you're running as root
# options.add_argument("--disable-dev-shm-usage")  # Supera las limitaciones de recursos en contenedores
options.add_experimental_option('useAutomationExtension', False)
# headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")

nap1 = 1

#%%

email = 'lilianpintor97@gmail.com'
password = 'Triomaravilla2'


#%%

url = 'https://sso.garmin.com/portal/sso/en-US/sign-in?clientId=GarminConnect&service=https%3A%2F%2Fconnect.garmin.com%2Fmodern'

driver = webdriver.Chrome(options=options)
driver.get(url)

stage_name = '1'

email_input_xpath = '//*[@id="email"]'

# email_input_field = driver.find_element(By.XPATH, email_input_xpath)

# email_input_field = EC.visibility_of_element_located((By.XPATH, email_input_xpath))

time.sleep(3)

email_input_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, email_input_xpath))
)


time.sleep(3)

email_input_field.send_keys(email)


password_input_xpath = '//*[@id="password"]'

password_input_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, password_input_xpath))
)


time.sleep(3)

password_input_field.send_keys(password)

enter_button_xpath = '//*[@id="portal"]/div[2]/div/div/div/div/form/section[2]/g-button/button'

enter_button = WebDriverWait(driver, nap1).until(EC.element_to_be_clickable((By.XPATH, enter_button_xpath)))

enter_button.click()

time.sleep(3)

forma_fisica_xpath = '/html/body/div/nav/div/ul[2]/li[2]/a'

forma_fisica_boton = WebDriverWait(driver, nap1).until(EC.element_to_be_clickable((By.XPATH, forma_fisica_xpath)))

forma_fisica_boton.click()

sueño_xpath = '/html/body/div/nav/div/ul[2]/li[2]/ul/li[1]/a'

sueño_boton = WebDriverWait(driver, nap1).until(EC.element_to_be_clickable((By.XPATH, sueño_xpath)))

sueño_boton.click()

time.sleep(3)

#hasta aqui todo bien

año_sueño_xpath = '//*[@id="pageContainer"]/div/div[1]/div/div/div/div[4]/div/ul/li[4]'

año_sueño_boton = WebDriverWait(driver, nap1).until(EC.element_to_be_clickable((By.XPATH, año_sueño_xpath)))

año_sueño_boton.click()


# Scrolling 
bottom = False
num_trys = 0    
while not bottom:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    num_trys += 1
    if num_trys > 5:
        bottom = True
    time.sleep(1)  # pause to make sure the page load with success

time.sleep(nap1)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


iframe = driver.find_element(By.TAG_NAME, "iframe")
driver.switch_to.frame(iframe)

# Intentar hacer scroll dentro del iframe
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# try:
#     WebDriverWait(driver, nap1).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
#     logging.info(f'{stage_name} done: Button clicked')
# except TimeoutException:
#     logging.info(f'{stage_name} done with no button click: Element not clickable within {nap1} seconds')
# except Exception as e:
#     logging.error(f'Unexpected error during {stage_name}: {e}')
# finally:
#     time.sleep(nap1)
