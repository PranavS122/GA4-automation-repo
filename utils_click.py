import re
import time
import json
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import chromedriver_autoinstaller


class doubleQuoteDict(dict):
    def __str__(self):
        return json.dumps(self)

    def __repr__(self):
        return json.dumps(self)


def is_element_visible(driver, xpath):
    try:
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return True
    except TimeoutException:
        return False

###########################################################################################
"""
This section stores all the selenium driver functions for performing GA4 site clicks
"""
###########################################################################################

class PageClick_GA():

    @staticmethod

    def selenium_honda_script(url, xpath_list):
        chromedriver_autoinstaller.install()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")

        options = {'backend': 'mitmproxy'}

        driver = webdriver.Chrome(seleniumwire_options=options, chrome_options=chrome_options)
        driver.get(url)

        accept_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']")))
        accept_button.click()
        print("Reached the target URL and accepted cookies")

        for xpath in xpath_list:
            element_found = False

            while not element_found:

                if is_element_visible(driver, xpath):
                    element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    time.sleep(10)
                    element.click()
                    print("Element found and clicked")
                    element_found = True
                    time.sleep(2)

                else:
                    print("Element not found within the visible screen, scrolling the screen")
                    driver.execute_script("window.scrollBy(0, 200)")

            
            params_list = []
            params_dict = {}
            for request in driver.requests:
                if request.url.startswith("https://www.google-analytics.com") and re.search(r"v=2", request.url):
                    params_dict = request.params.copy()
                    params_list.append(params_dict)
                
        return params_list
    

    def selenium_ee_script(url, xpath_list):   # EE phonesmart script under-development for errors

        chromedriver_autoinstaller.install()

        options = {'backend': 'mitmproxy'}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(seleniumwire_options=options, chrome_options=chrome_options)
        driver.get(url)

        time.sleep(10)
        accept_button = driver.find_element(By.XPATH,
                                            "//button[contains(@data-analytics, 'cookieOverlay')]/span[@class='lc-Button lc-ButtonEE']")
        time.sleep(10)
        accept_button.click()
        time.sleep(10)
        print("Reached the target url and accepted cookies")

        for xpath in xpath_list:
            element_found = False

            while not element_found:
                if is_element_visible(driver, xpath):
                    element = WebDriverWait(driver, 80).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    time.sleep(15)
                    element.click()
                    print("Element found and clicked")
                    element_found = True
                    time.sleep(15)
                else:
                    print("Element not found within the visible screen, scrolling the screen")
                    driver.execute_script("window.scrollBy(0, 200)")

            params_list = []
            params_dict = {}
            for request in driver.requests:
                if request.url.startswith("https://www.google-analytics.com") and re.search(r"v=2", request.url):
                    params_dict = request.params.copy()
                    params_list.append(params_dict)

        return params_list
        

    def selenium_formula_script(url, xpath_list):

        chromedriver_autoinstaller.install()
        options = {
        'backend': 'mitmproxy'}

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(seleniumwire_options=options, chrome_options=chrome_options)
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        time.sleep(20)
        iframe_element = wait.until(EC.presence_of_element_located((By.ID, "sp_message_iframe_877301")))
        time.sleep(20)
        driver.switch_to.frame(iframe_element)
        accept_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]/button[2]')
        time.sleep(20)
        accept_button.click()

        print("Reached the target URL and accepted cookies")

        for xpath in xpath_list:
            element_found = False

            while not element_found:

                if is_element_visible(driver, xpath):
                    element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    element.click()
                    print("Element found and clicked")
                    element_found = True
                    time.sleep(15)

                else:
                    print("Element not found within the visible screen, scrolling the screen")
                    driver.execute_script("window.scrollBy(0, 200)")

            time.sleep(5)
            params_list = []
            params_dict = {}
            for request in driver.requests:
                if request.url.startswith("https://www.google-analytics.com") and re.search(r"v=2", request.url):
                    params_dict = request.params.copy()
                    params_list.append(params_dict)
                
        return params_list




    

###########################################################################################
"""
This section stores all the selenium driver functions for performing adobe site clicks
"""
###########################################################################################

class PageClick_Adobe():

    def selenium_goodyear_script(url, xpath_list):

        chromedriver_autoinstaller.install()

        options = {
        'backend': 'mitmproxy'}

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options, chrome_options=chrome_options)
        driver.get(url)

        wait = WebDriverWait(driver, 20)
        accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']")))
        accept_button.click()
        print("Reached the target URL and accepted cookies")
        time.sleep(20)

        for xpath in xpath_list:
            element_found = False

            while not element_found:

                if is_element_visible(driver, xpath):
                    element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    element.click()
                    print("Element found and clicked")
                    element_found = True
                    time.sleep(15)

                else:
                    print("Element not found within the visible screen, scrolling the screen")
                    driver.execute_script("window.scrollBy(0, 200)")

            time.sleep(10)
            params_list = []
            params_dict = {}
            for request in driver.requests:
                if request.url.startswith("https://goodyear.d2.sc.omtrdc.net") and re.search(r"b/ss", request.url):
                    params_dict = request.params.copy()
                    params_list.append(params_dict)
                
        return params_list