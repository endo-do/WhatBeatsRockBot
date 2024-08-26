import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pathlib
import customtkinter as ctk
import threading
import time

CHROMEDRIVER_PATH = r"C:\\Users\\anmel\\OneDrive\\Desktop\\chromedriver-win32\\chromedriver.exe"
WEBSITE_PATH = "https://www.whatbeatsrock.com"
DIR_PATH = pathlib.Path().resolve()

stop_event = threading.Event()
threads = []

def on_close():
    print("on close")
    stop_threads()
    app.quit()

def stop_threads():
    print("stop threads")
    stop_event.set()
    print(stop_event)

app = ctk.CTk()
app.geometry("600x400")
app.title("Terminal")

output_textbox = ctk.CTkTextbox(app, width=600, height=400)
output_textbox.pack(pady=10, padx=10)

app.protocol("WM_DELETE_WINDOW", on_close)

output_textbox.tag_config("info", foreground="white")
output_textbox.tag_config("success", foreground="#00FF00")
output_textbox.tag_config("correct", foreground="green")
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
    output_textbox.insert("end", str(id) + ": " + msg + end, tag)
    output_textbox.see("end")

def main(id):

    id += 1

    with open(DIR_PATH.joinpath("Words.txt"), "r") as f:
        words = [i.strip("\n") for i in f.readlines()]
        words = remove_duplicates(words)
        log_message("Word List loaded", id, tag="success")

    service = Service(executable_path=CHROMEDRIVER_PATH)

    driver = webdriver.Chrome(service=service)
    log_message("Chrome Driver initialized", id, tag="success")

    driver.get(WEBSITE_PATH)
    log_message("Website loaded", id, tag="success")

    log_message("Starting to insert words", id, tag="warning")
    prev_word = "Rock"
    for word in words:

        if stop_event.is_set():
            driver.quit()

        input_field = driver.find_element(By.CSS_SELECTOR, ".pl-4.py-4.text-lg.border.border-1-black")
        input_field.clear()
        input_field.send_keys(word)
        input_field.send_keys(Keys.RETURN)
        # log_message(f"{word} ", end="", tag="note")
        # log_message(f"vs ", end="", tag="info")
        # log_message(f"{last_word}", end=": ", tag="note2")
        
        correct = None
        while True:

            if stop_event.is_set():
                driver.quit()

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

        if stop_event.is_set():
            driver.quit()

        if correct:
            # log_message(f"Correct", tag="correct")
            prev_word = word
            button_field.send_keys(Keys.RETURN)

        else:
            log_message(f"{word} does not beat {prev_word}", id, tag="error")
            driver.quit()

    log_message("Ran out of Words", id, tag="warning")

for i in range(1):
    thread = threading.Thread(target=main, args=(i,), daemon=True)
    threads.append(thread)
    thread.start()

app.mainloop()