import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Credentials
username = "lalasmuathasim@gmail.com"
password = "1Thahomas#"

# initialise the Chrome driver
driver = webdriver.Chrome(chrome_options=chrome_options)

# Click the link from the first page
driver.get("https://tax.lsgkerala.gov.in/epayment/")
driver.find_element("link text", "Payment for Registered Users").click()

# Input the Username and Password in the login page
driver.find_element("id", "txtUsername").send_keys(username)
driver.find_element("id", "params").send_keys(password)
time.sleep(10)
driver.find_element("name", "btnSearch").click()

# Click on the enroll building
driver.find_element("link text", "Enroll a Building").click()

driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div/table/tbody/tr[5]/td/div/table/tbody/tr[947]/td[2]/div/input").click()

# Select the ward and input building number
# Initiate a dictionary
data = dict()
for x in range(1000):
    ward_year = Select(driver.find_element("id", "cmbWardYear"))
    ward_year.select_by_visible_text("2013")
    driver.find_element("id", "txtWard").send_keys("22")
    driver.find_element("id", "txtODNo").send_keys(x+1)

    driver.find_element("name", "btnSearch").click()
    print(x+1)

    element = driver.find_elements(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div/table/tbody/tr[4]/td/div[1]/div/table/tbody/tr[6]/td[2]/div")
    no_of_element = len(element)

    if no_of_element > 0:
        elem = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div/table/tbody/tr[4]/td/div[1]/div/table/tbody/tr[6]/td[2]/div")
        data[x] = elem.text
        # print(elem.text)

    driver.find_element("id", "txtWard").clear()
    driver.find_element("id", "txtODNo").clear()

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

WebDriverWait(driver=driver, timeout=10).until(lambda x: x.execute_script("return document.readyState === 'complete'"))
error_message = "Incorrect Username or Password"
errors = driver.find_elements("css selector", ".error-msg")

if any(error_message in e.text for e in errors):
    print("[!] Login failed", errors)
else:
    print("[+] Login successful")

