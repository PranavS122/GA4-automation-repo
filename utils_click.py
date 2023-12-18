import re
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

class PageClick():

    def selenium_honda_script(url, user_xpath):
        options = {
        'backend': 'mitmproxy'}

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("-headless")

        driver = webdriver.Chrome(options=options, chrome_options=chrome_options)


        driver.get(url)

        accept_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']")))
        accept_button.click()
        print("Reached the target URL and accepted cookies")
        element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, user_xpath)))
        time.sleep(5)
        element.click()
        time.sleep(10)

        params_dict = {}

        for idx, request in enumerate(driver.requests, start=1):
                if request.url.startswith("https://www.google-analytics.com/g/collect") and re.search(r'en=configurator&', request.url):
                    print(f"GA4 collect call {idx} intercepted, Parameters collected")
                    params_dict[idx] = request.params

        return params_dict