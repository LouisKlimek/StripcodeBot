from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import os
import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
import time
import random

username = "YOUR_USERNAME_HERE"
password = "YOUR_PASSWORD_HERE"


chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--window-size=1920x1080")
# For older ChromeDriver under version 79.0.3945.16
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

#For ChromeDriver version 79.0.3945.16 or over
chrome_options.add_argument('--disable-blink-features=AutomationControlled')


driver = webdriver.Chrome(options=chrome_options)

# load the desired webpage
driver.get('https://stripcode.dev/ranked')


# find username/email field and send the username itself to the input field
driver.find_element_by_id("login_field").send_keys(username)
# find password input field and insert password as well
driver.find_element_by_id("password").send_keys(password)
# click login button
driver.find_element_by_name("commit").click()

time.sleep(4)
while True:
    time.sleep(random.randint(1, 2))
    filename = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/h1").text

    i = 0
    for repository in driver.find_elements_by_class_name("mb-4"):
        try:
            repositoryUrl = "https://github.com/" + repository.find_elements_by_tag_name('button')[0].find_elements_by_tag_name('span')[0].text
            code = driver.find_element_by_xpath('//*[@id="main-code-block"]').text

            time.sleep(2)
            html = requests.get(repositoryUrl + "/search?q=filename%3A" + filename).text
            soup = BeautifulSoup(html, "html.parser")

            if "hx_hit-code code-list-item d-flex py-4 code-list-item-public repo-specific" in html:
                # Found File in this repository
                repository.find_elements_by_tag_name('button')[0].click()
                print("Found File in " + repositoryUrl)
                break
            else:
                # Could not find File in this repository
                print("File not found in " + repositoryUrl)
        except:
            pass

        i = i + 1
    print("--------------------------------")

    # Go to next Question
    time.sleep(random.randint(2, 3))
    while not driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[2]/div[1]/button"):
		# Just click the last option if nothing could be found
        driver.find_elements_by_class_name("mb-4")[0].find_elements_by_tag_name('button')[0].click()
        time.sleep(2)
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[1]/button").click()

time.sleep(100)
driver.close()