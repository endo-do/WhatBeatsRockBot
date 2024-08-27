import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import pathlib
import customtkinter as ctk
import threading
import time

CHROMEDRIVER_PATH = r"C:\\Users\\anmel\\OneDrive\\Desktop\\chromedriver-win32\\chromedriver.exe"
WEBSITE_PATH = "https://www.whatbeatsrock.com"
DIR_PATH = pathlib.Path().resolve()

choices = ["paper",  "scissor", "rock"]
threads = []

app = ctk.CTk()
app.geometry("600x400")
app.title("Terminal")

output_textbox = ctk.CTkTextbox(app, width=600, height=400)
output_textbox.pack(pady=10, padx=10)

output_textbox.tag_config("info", foreground="black")
output_textbox.tag_config("success", foreground="green")
output_textbox.tag_config("correct", foreground="#00FF00")
output_textbox.tag_config("warning", foreground="orange")
output_textbox.tag_config("error", foreground="red")
output_textbox.tag_config("note", foreground="#2b55e2")
output_textbox.tag_config("note2", foreground="#b82be2")

def remove_duplicates(list):
    clean_list = []
    for i in list:
        if i not in clean_list:
            clean_list.append(i)
    
    return clean_list

def log_message(msg, id, tag="info", end="\n"):
    output_textbox.insert("end", "Instance "+ str(id) + ": " + msg + end, tag)
    output_textbox.see("end")

def main(id):

    id += 1

    with open(DIR_PATH.joinpath("Names.txt"), "r") as f:
        content = [i.strip("\n") for i in f.readlines()]
        content = [i.strip(" ") for i in content]
        names = []
        for i in content:
            names.append(f"A Person named {i} plays Paper")
            names.append(f"A Person named {i} plays Scissor")
            names.append(f"A Person named {i} plays Rock")
        log_message("Word List loaded", id, tag="success")
        for i in names:
            print(i)

    service = Service(executable_path=CHROMEDRIVER_PATH)

    driver = webdriver.Chrome(service=service)
    log_message("Chrome Driver initialized", id, tag="success")

    driver.get(WEBSITE_PATH)
    log_message("Website loaded", id, tag="success")

    log_message("Starting to insert words", id, tag="warning")

    prev_word = "Rock"
    score = 0
    for index, name in enumerate(names):

        input_field = driver.find_element(By.CSS_SELECTOR, ".pl-4.py-4.text-lg.border.border-1-black")
        input_field.clear()
        input_field.send_keys(name)
        input_field.send_keys(Keys.RETURN)

        try:
            time.sleep(0.5)
            alert = driver.switch_to.alert
            alert_text = alert.text
            log_message(f"Alert: {alert_text}", id, tag="error")
            log_message(f"Score: {score}", id)
            input()
            service.quit()

        except NoAlertPresentException:
            pass
        
        correct = None
        while True:

            try:
                button_field = driver.find_element(By.CSS_SELECTOR, ".py-4.px-8.border.border-1-black.text-lg")
                correct = True
                break
        
            except selenium.common.exceptions.NoSuchElementException:
                pass
            
            try:
                button_field = driver.find_element(By.CSS_SELECTOR, ".p-2.px-4.border.border-1-black.text-lg")
                correct = False
                break
        
            except selenium.common.exceptions.NoSuchElementException:
                pass

            time.sleep(0.5)

        if correct:
            prev_word = name
            score += 1
            button_field.send_keys(Keys.RETURN)

        else:
            log_message(f"{name} {choices[i]} does not beat {prev_word} {choices[i-1%3]}", id, tag="error")
            score = driver.find_element(By.CSS_SELECTOR,  "p.text-gray-500").text.split(": ")[1]
            log_message(f"Score: {score}", id)
            input()
            driver.quit()

    log_message("Ran out of Words", id, tag="warning")
    log_message(f"Score: {score}", id)

for i in range(1):
    thread = threading.Thread(target=main, args=(i,), daemon=True)
    threads.append(thread)
    thread.start()

app.mainloop()