import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Установка ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Разворачивание окна на весь экран
driver.maximize_window()

# Открытие страницы
driver.get("https://my.sdu.edu.kz/")

# Пауза для загрузки страницы
time.sleep(5)

# Ввод имени пользователя
username = driver.find_element(By.ID, "username")
username.send_keys("220103362")


time.sleep(5)

# Ввод пароля
password = driver.find_element(By.ID, "password")
password.send_keys("Krbv_002")

time.sleep(5)

# Нажатие Enter (если нужно)
password.send_keys(Keys.ENTER)

# Закрытие браузера (можно убрать, если не нужно)
time.sleep(5)

button = driver.find_element(By.LINK_TEXT,"[ Sign out ]")
button.click()
time.sleep(10)

driver.quit()
