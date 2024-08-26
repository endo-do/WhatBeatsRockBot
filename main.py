import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pathlib

CHROMEDRIVER_PATH = r"C:\\Users\\anmel\\OneDrive\\Desktop\\chromedriver-win32\\chromedriver.exe"
WEBSITE_PATH = "https://www.whatbeatsrock.com"
DIR_PATH = pathlib.Path().resolve()

def remove_duplicates(list):
    clean_list = []
    for i in list:
        if i not in clean_list:
            clean_list.append(i)
    
    return clean_list

with open(DIR_PATH.joinpath("Words.txt"), "r") as f:
    words = [i.strip("\n") for i in f.readlines()]
    words = remove_duplicates(words)
    print("Words loaded")

service = Service(executable_path=CHROMEDRIVER_PATH)

driver = webdriver.Chrome(service=service)

driver.get(WEBSITE_PATH)
print("Website opened")

for word in words:

    try:

        input_field = driver.find_element(By.CSS_SELECTOR, ".pl-4.py-4.text-lg.border.border-1-black")
        input_field.clear()
        input_field.send_keys(word)
        input_field.send_keys(Keys.RETURN)
        while True:
            try:
                button_field = driver.find_element(By.CSS_SELECTOR, ".py-4.px-8.border.border-1-black.text-lg")
                break
            except selenium.common.exceptions.NoSuchElementException:
                pass
        button_field.send_keys(Keys.RETURN)

    except selenium.common.exceptions.NoSuchElementException:
        break

input()