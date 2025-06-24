from selenium import webdriver
from selenium.webdriver.common.by import By
import time, pickle, os

def linkedin_login(username, password, cookies_path='cookies.pkl'):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=options)
    
    driver.get('https://www.linkedin.com/login')
    
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    # driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(5)  # 2FA wait or redirect

    cookies = driver.get_cookies()
    with open(cookies_path, 'wb') as f:
        pickle.dump(cookies, f)
    
    driver.quit()
    return cookies
