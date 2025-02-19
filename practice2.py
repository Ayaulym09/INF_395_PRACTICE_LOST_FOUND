import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.maximize_window()
driver.get("https://alser.kz/")

time.sleep(5)

button_yes = driver.find_element(By.CSS_SELECTOR, "button.green-text.label-large.spacer.selectable")


time.sleep(5)
button_yes.click()


account_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/header/div/div[2]/div[4]/div[4]/a/svg/g/path[1]")

account_button.click()

time.sleep(10)



email_input = driver.find_element(By.XPATH, "/html/body/div[2]/div/main/div[2]/div/div[2]/section/form/div[1]/input")
email_input.click()


email_input.send_keys('87057789928')

time.sleep(5)

password = driver.find_element('/html/body/div[2]/div/main/div[2]/div/div[2]/section/form/div[2]/div[1]/input')
password.send_keys("ayau_002")

time.sleep(5)

button = driver.find_element(By.XPATH,'/html/body/div[2]/div/main/div[2]/div/div[2]/section/form/div[4]/button')
button.click()
