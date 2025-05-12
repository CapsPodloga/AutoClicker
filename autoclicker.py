import threading
import time
import customtkinter as ctk
from pynput import mouse, keyboard

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AutoClicker:
    def __init__(self):
        self.clicking = False
        self.cps = 10
        self.hotkey = keyboard.Key.f6  # domyślny skrót
        self.mouse = mouse.Controller()
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def click_loop(self):
        while self.clicking:
            self.mouse.click(mouse.Button.left)
            time.sleep(1 / self.cps)

    def on_key_press(self, key):
        if key == self.hotkey:
            self.toggle_clicking()

    def toggle_clicking(self):
        self.clicking = not self.clicking
        if self.clicking:
            threading.Thread(target=self.click_loop, daemon=True).start()

    def set_cps(self, value):
        self.cps = value

    def set_hotkey(self, key):
        self.hotkey = key

clicker = AutoClicker()

# Interfejs (syzyf)
app = ctk.CTk()
app.title("AutoClicker")
app.geometry("400x260")

def update_cps(value):
    clicker.set_cps(int(float(value)))
    cps_label.configure(text=f"{int(float(value))} CPS")

def set_new_hotkey():
    def on_press(key):
        clicker.set_hotkey(key)
        try:
            key_name = key.char.upper()
        except:
            key_name = str(key).replace("Key.", "").upper()
        hotkey_label.configure(text=f"Skrót: {key_name}")
        listener.stop()

    hotkey_label.configure(text="Wciśnij nowy klawisz...")
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

title = ctk.CTkLabel(app, text="AutoClicker", font=ctk.CTkFont(size=20, weight="bold"))
title.pack(pady=(10,0))

credits = ctk.CTkLabel(app, text="Made by Caps_", font=ctk.CTkFont(size=10, slant="italic"), text_color="#888888")
credits.pack(pady=(0,10))

cps_label = ctk.CTkLabel(app, text="10 CPS")
cps_label.pack()

cps_slider = ctk.CTkSlider(app, from_=1, to=50, number_of_steps=49, command=update_cps)
cps_slider.set(10)
cps_slider.pack(pady=5)

hotkey_label = ctk.CTkLabel(app, text="Skrót: F6")
hotkey_label.pack(pady=5)

change_hotkey_btn = ctk.CTkButton(app, text="Zmień skrót", command=set_new_hotkey)
change_hotkey_btn.pack(pady=5)

info = ctk.CTkLabel(app, text="Użyj skrótu, aby włączyć/wyłączyć.")
info.pack(pady=10)

app.mainloop()
