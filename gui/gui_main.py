import tkinter as tk
from tkinter import messagebox
import threading, time
from core import screen_capture, ocr_engine, leak_detector, obs_controller, nsfw_detector
import json

with open("config.json") as f:
    config = json.load(f)

def monitor():
    while True:
        img = screen_capture.capture_screen()
        text = ocr_engine.extract_text_from_image(img)

        if leak_detector.contains_leak(text):
            print("Leak Detected!")
            obs_controller.trigger_obs_scene()

        if nsfw_detector.is_nsfw(img):
            print("NSFW Detected!")
            obs_controller.trigger_obs_scene()

        time.sleep(config.get("scan_interval_sec", 3))

def run_gui():
    root = tk.Tk()
    root.title("LeakBlock")

    label = tk.Label(root, text="LeakBlock is running...", font=("Arial", 14))
    label.pack(pady=20)

    def start_monitoring():
        threading.Thread(target=monitor, daemon=True).start()
        messagebox.showinfo("LeakBlock", "Monitoring started.")

    btn_start = tk.Button(root, text="Start Monitoring", command=start_monitoring)
    btn_start.pack(pady=10)

    root.mainloop()
