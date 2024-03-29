import re
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver
import chromedriver_autoinstaller

class doubleQuoteDict(dict):
    def __str__(self):
        return json.dumps(self)

    def __repr__(self):
        return json.dumps(self)


########################################################################################
"""
This section contains all the selenium scripts for GA4 parameters testing for page_view
"""
########################################################################################

class PageSelector():

    def selenium_honda_script(url):

        chromedriver_autoinstaller.install()
        options = {
        'backend': 'mitmproxy'}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("-headless")
        driver = webdriver.Chrome(options=options, chrome_options=chrome_options)
        driver.get(url)

        wait = WebDriverWait(driver, 20)
        accept_button = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']")))
        accept_button.click()
        print("Reached the target URL and accepted cookies")
        time.sleep(20)

        params_dict = {}

        for idx, request in enumerate(driver.requests, start=1):
            if request.url.startswith("https://www.google-analytics.com/g/collect") and re.search(r'en=page_view', request.url):
                print(f"GA4 collect call {idx} intercepted, Parameters collected")
                params_dict[idx] = request.params

        return params_dict
    
    def selenium_ee_script(url):

        chromedriver_autoinstaller.install()
        options = {
        'backend': 'mitmproxy'}

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("-headless")
        driver = webdriver.Chrome(options=options, chrome_options=chrome_options)
        driver.get(url)

        time.sleep(10)
        accept_button = driver.find_element(By.XPATH,
                                            "//button[contains(@data-analytics, 'cookieOverlay')]/span[@class='lc-Button lc-ButtonEE']")
        time.sleep(10)
        accept_button.click()
        time.sleep(10)
        print("Reached the target url and accepted cookies")

        time.sleep(20)

        params_dict = {}

        for idx, request in enumerate(driver.requests, start=1):
            if request.url.startswith("https://www.google-analytics.com/g/collect") and re.search(r'en=page_view', request.url):
                print(f"GA4 collect call {idx} intercepted, Parameters collected")
                params_dict[idx] = request.params

        return params_dict
    
    def selenium_formula_script(url):

        chromedriver_autoinstaller.install()
        options = {
        'backend': 'mitmproxy'}

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=options, chrome_options=chrome_options)
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        time.sleep(20)
        iframe_element = wait.until(ec.presence_of_element_located((By.ID, "sp_message_iframe_877301")))
        time.sleep(20)
        driver.switch_to.frame(iframe_element)
        accept_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]/button[2]')
        time.sleep(20)
        accept_button.click()

        print("Reached the target URL and accepted cookies")
        time.sleep(30)

        params_dict = {}

        for idx, request in enumerate(driver.requests, start=1):
            if request.url.startswith("https://www.google-analytics.com/g/collect") and re.search(r'en=page_view', request.url):
                print(f"GA4 collect call {idx} intercepted, Parameters collected")
                params_dict[idx] = request.params

        return params_dict
    

#########################################################################
"""
This section contains all the code for testing adobe analytis parameters
"""
#########################################################################  

class PageSelector_Adobe():

    def selenium_goodyear_script(url):

        chromedriver_autoinstaller.install()

        options = {
        'backend': 'mitmproxy'}

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("-headless")
        driver = webdriver.Chrome(options=options, chrome_options=chrome_options)
        driver.get(url)

        wait = WebDriverWait(driver, 20)
        accept_button = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']")))
        accept_button.click()
        print("Reached the target URL and accepted cookies")
        time.sleep(20)

        params_dict = {}

        for idx, request in enumerate(driver.requests, start=1):
            if request.url.startswith("https://goodyear.d2.sc.omtrdc.net") and re.search(r'b/ss', request.url):
                print(f"Adobe request call {idx} intercepted, Parameters collected")
                params_dict[idx] = request.params

        return params_dict


        

