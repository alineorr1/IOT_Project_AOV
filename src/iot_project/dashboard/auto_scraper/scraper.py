#Libraries
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

import logging
#logging
logger = logging.getLogger('myAppLogger')

#%%

def dash_scraper(day: str, screenshot_path: str):
    """
    Parameters
    ----------
    day : str
        DESCRIPTION.
    screenshot_path : str
        DESCRIPTION.

    Returns
    -------
    None.
    day = '2024-12-06'
    screenshot_path = 'Output/dashboard_output'

    """    
    sleep = .03
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('window-size=1200x600')
    options.add_argument("start-maximized")
    
    driver = webdriver.Chrome(options=options)
    
    time.sleep(sleep)
    driver.get("http://127.0.0.1:8031/")
    time.sleep(sleep)
    
    boton_tache_dia = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="day-dropdown"]/div/div/span[1]')))
    
    time.sleep(sleep)
    boton_tache_dia.click()
    time.sleep(sleep)
    
    logger.info('done')
    time.sleep(sleep)
    
    day_text = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-select-2--value"]/div[2]/input')))
    time.sleep(sleep)
    
    day_text.send_keys(day)
    time.sleep(sleep)
    
    day_text.send_keys(Keys.ENTER)
    time.sleep(sleep)
    
    submit = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-button"]'))).click()

    element = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="page-content"]/div/div'))
    )
    time.sleep(3)
    
    # Use Chrome DevTools to capture the full page.
    driver.execute_script("document.body.style.zoom='100%'")
    result = driver.execute_cdp_cmd("Page.captureScreenshot", {
        "format": "png",
        "fromSurface": True,
        "captureBeyondViewport": True
    })
    with open(screenshot_path, "wb") as f:
        f.write(base64.b64decode(result['data']))
    time.sleep(sleep)
    
    return None
