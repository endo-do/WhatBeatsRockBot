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
automate = True

app = ctk.CTk()
app.geometry("600x400")
app.title("Terminal")

output_textbox = ctk.CTkTextbox(app, width=600, height=350)
output_textbox.pack(pady=0, padx=5)

input_entry = ctk.CTkEntry(app, width=600, height=40, placeholder_text="Console: ")
input_entry.pack(pady=0, padx=5)
input_entry.bind("<Return>", lambda event: on_enter_press())

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

def on_enter_press():
    user_input_comit.set()

def log_message(msg, id=1, tag="info", end="\n"):
    output_textbox.insert("end", "Instance "+ str(id) + f" {time.strftime("%H:%M:%S", time.localtime())}: " + msg + end, tag)
    output_textbox.see("end")

def num_to_id(num):
    letters = ["a", "b", "e", "d", "u", "f", "o", "t", "i", "s"]
    id = ""
    for i in str(num):
        id += letters[int(i)]

    return id

def main(id):

    names = []
    
    for i in range(1000, 2501):
        names.append(f"A Robot named {num_to_id(i)} plays Paper")
        names.append(f"A Robot named {num_to_id(i)} plays Scissor")
        names.append(f"A Robobt named {num_to_id(i)} plays Rock")
    log_message("Input List Generated", id, tag="success")

    service = Service(executable_path=CHROMEDRIVER_PATH)

    driver = webdriver.Chrome(service=service)
    log_message("Chrome Driver initialized", id, tag="success")

    driver.get(WEBSITE_PATH)
    log_message("Website loaded", id, tag="success")

    log_message("Starting to insert words", id, tag="warning")

    prev_word = "Rock"
    score = 0
    for name in names:

        pause = False
        if user_input_comit.is_set():
            pause = True
            while pause:
                user_input_comit.clear()
                user_input = input_entry.get()
                input_entry.delete(0, ctk.END)
                log_message(f"Captured user Input: '{user_input}'", id, tag="note")
                if user_input == "pause":    
                    log_message(f"Pausing Script ...", id, tag="warning")
                    log_message(f"Score: {score}", id)
                    log_message(f"Type 'continue' to continue", id)
                    while not user_input_comit.is_set():
                        time.sleep(0.5)
                    user_input = input_entry.get()
                    user_input_comit.clear()
                    log_message(f"Captured user Input: '{user_input}'", id, tag="note")
                    input_entry.delete(0, ctk.END)
                    if user_input == "continue":
                        log_message("Continuingt the script ...", id, tag="warning")
                        pause = False
                        break
                
                elif user_input == "quit":
                    log_message("Quitting programm and all drivers ...", id, tag="error")
                    time.sleep(1)
                    driver.quit()
                    app.quit()
            
                else:
                    pause = False
                    break

        input_field = driver.find_element(By.CSS_SELECTOR, ".pl-4.py-4.text-lg.border.border-1-black")
        input_field.clear()
        input_field.send_keys(name)
        input_field.send_keys(Keys.RETURN)

        alert = None
        try:
            time.sleep(0.5)
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()

        except NoAlertPresentException:
            pass

        while alert:
            user_input_comit.clear()
            log_message(f"Alert: {alert_text}", id, tag="error")
            
            if alert_text == "rate limit exceeded! slow down or dm us on discord/twitter" and automate:
                log_message(f"Waiting 1h to wait out rate limit and continue programm afterwards", id, tag="warning")
                time.sleep(3601)
                log_message(f"Continuing the programm", id, tag="warning")
                alert=None
                break

            else:
                
                log_message(f"Score: {score}", id)
                log_message(f"To try to continue the programm type 'continue'", id)
                log_message(f"To quit type anything", id)
                while not user_input_comit.is_set():
                    time.sleep(0.5)
                user_input = input_entry.get()
                log_message(f"Captured user Input: '{user_input}'", id, tag="note")
                input_entry.delete(0, ctk.END)
                if user_input == "continue":
                    log_message("Continuing the programm", id, tag="warning")
                    input_field.send_keys(Keys.RETURN)
                    
                    try:
                        time.sleep(0.5)
                        alert = driver.switch_to.alert
                        alert_text = alert.text
                        alert.accept()

                    except NoAlertPresentException:
                        alert = None
                        break
                
                else:
                    log_message("Quitting programm and all drivers ...", id, tag="error")
                    time.sleep(1)
                    driver.quit()
                    app.quit()

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
            log_message(f"{name} does not beat {prev_word}", id, tag="error")
            score = driver.find_element(By.CSS_SELECTOR,  "p.text-gray-500").text.split(": ")[1]
            log_message(f"Score: {score}", id)
            input()
            driver.quit()

    log_message("Ran out of Words", id, tag="warning")
    log_message(f"Score: {score}", id)

user_input_comit = threading.Event()
thread = threading.Thread(target=main, args=(1,), daemon=True)
thread.start()

app.mainloop()