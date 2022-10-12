from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
import datetime
import re
import os
import json
import time

if __name__ == '__main__':
    with open('config.json') as config:
        config_data = json.load(config)

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                         "like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.67 (Edition Yx 05)")
    options.add_argument(f'--user-data-dir={config_data["user-data-dir"]}')
    options.add_argument(f'--profile-directory={config_data["profile-directory"]}')

    s = Service(r"chromedriver\chromedriver.exe")
    driver = webdriver.Chrome(service=s,
                              options=options)
    stealth(driver,
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    if not os.path.exists((os.path.join(config_data['csv_save_path'], 'ozon_data.csv'))):
        with open((os.path.join(config_data['csv_save_path'], 'ozon_data.csv')), 'w') as f:
            f.write('Name|Colour|Seller|Remainder|Date\n')

    driver.get("https://www.ozon.ru/cart")
    # bucket = driver.find_element(By.XPATH, '//*[@id="stickyHeader"]/div[4]/a[2]/span[2]')
    # time.sleep(4)
    # bucket.click()
    positions_amount = len(driver.find_elements(By.XPATH,
                                                '//*[@id="layoutPage"]/div[1]/div/div/div[3]/div[4]/div[1]/div['
                                                '1]/div/div[2]/div'))
    for position in range(2, positions_amount + 1):
        chars_amount = len(driver.find_elements(By.XPATH,
                                                f'//*[@id="layoutPage"]/div[1]/div/div/div[3]/div[4]/div[1]/div['
                                                f'1]/div/div[2]/div[{position}]/div[1]/div/div/div/div[2]/a/span'))

        name = driver.find_element(By.XPATH,
                                   f'//*[@id="layoutPage"]/div[1]/div/div/div[3]/div[4]/div[1]/div[1]/div/div[2]/div[{position}]/div[1]/div/div/div/div[2]/a/span[1]/span').text
        if chars_amount > 2:
            colour = driver.find_element(By.XPATH,
                                         f'//*[@id="layoutPage"]/div[1]/div/div/div[3]/div[4]/div[1]/div[1]/div/div['
                                         f'2]/div[{position}]/div[1]/div/div/div/div[2]/a/span[2]/span').text
        else:
            colour = '-'
        seller = driver.find_element(By.XPATH,
                                     f'//*[@id="layoutPage"]/div[1]/div/div/div[3]/div[4]/div[1]/div[1]/div/div[2]/div[{position}]/div[1]/div/div/div/div[2]/a/span[{chars_amount}]/span').text

        amount = driver.find_element(By.XPATH,
                                     f'//*[@id="layoutPage"]/div[1]/div/div/div[3]/div[4]/div[1]/div[1]/div/div[2]/div[{position}]/div[2]/div/div[1]/div/div/div[1]/div/div/input')
        amount.click()
        ost = -1
        try:
            WebDriverWait(driver, 2.5).until(EC.element_to_be_clickable((By.XPATH,
                                                                       "//*[contains(text(), '10+')]"))).click()
        except:
            ost = '<10'
            amount.click()

        if ost != -1:
            left = '<10'

        else:
            ostatok = driver.find_element(By.XPATH,
                                          f'//*[@id="layoutPage"]/div[1]/div/div/div[3]/div[4]/div[1]/div[1]/div/div['
                                          f'2]/div[{position}]/div[2]/div/div[2]/span/span')
            ostatok_data = ostatok.text
            if ostatok_data == 'Осталось 100+':
                max = driver.find_element(By.XPATH,
                                          f'//*[@id="layoutPage"]/div[1]/div/div/div[3]/div[4]/div[1]/div[1]/div/div['
                                          f'2]/div[{position}]/div[2]/div/div[1]/div/input')
                left = max.get_attribute('max')
            else:
                left = re.findall(r'\d+', ostatok_data)[0]

        with open((os.path.join(config_data['csv_save_path'], 'ozon_data.csv')), 'a') as f:
            f.write(f'{name}|{colour}|{seller}|{left}|{datetime.datetime.now()}\n')

    driver.close()
    driver.quit()
