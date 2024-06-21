from selenium import webdriver
driver = webdriver.Chrome()  # если драйвер был для Chrome
driver.get("https://www.google.com")
print(driver.title)