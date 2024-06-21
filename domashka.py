from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def search_wikipedia(driver, query):
    driver.get("https://www.wikipedia.org/")
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys(query)
    search_box.submit()
    time.sleep(3)  # Ждем загрузки страницы

def list_paragraphs(driver):
    paragraphs = driver.find_elements(By.XPATH, "//div[@class='mw-parser-output']/p")
    for idx, paragraph in enumerate(paragraphs):
        print(f"Абзац {idx + 1}: {paragraph.text[:200]}...")  # Печатаем первые 200 символов

def list_internal_links(driver):
    links = driver.find_elements(By.XPATH, "//div[@class='mw-parser-output']//a[@href]")
    internal_links = [link for link in links if link.get_attribute("href").startswith("https://ru.wikipedia.org/wiki/")]
    for idx, link in enumerate(internal_links):
        print(f"{idx + 1}: {link.get_attribute('href')} - {link.text}")
    return internal_links

def main():
    driver = get_driver()

    try:
        while True:
            query = input("Введите запрос для поиска: ")

            search_wikipedia(driver, query)

            while True:
                print("\nЧто бы вы хотели сделать дальше?")
                print("1. Список абзацев текущей статьи")
                print("2. Перейти по одной из внутренних ссылок")
                print("3. Выйти")

                choice = input("Введите ваш выбор: ")

                if choice == "1":
                    list_paragraphs(driver)
                elif choice == "2":
                    internal_links = list_internal_links(driver)

                    link_choice = input("Введите номер ссылки, по которой хотите перейти: ")
                    try:
                        link_index = int(link_choice) - 1
                        if 0 <= link_index < len(internal_links):
                            driver.get(internal_links[link_index].get_attribute("href"))
                            time.sleep(3)  # Ждем загрузки страницы
                        else:
                            print("Неверный номер ссылки. Пожалуйста, попробуйте снова.")
                    except ValueError:
                        print("Пожалуйста, введите корректный номер.")
                elif choice == "3":
                    print("Выход...")
                    return
                else:
                    print("Неверный выбор. Пожалуйста, попробуйте снова.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
