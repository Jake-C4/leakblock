import tkinter as tk
from tkinter import messagebox
import threading, time
from core import screen_capture, ocr_engine, leak_detector, obs_controller, nsfw_detector
import json

with open("config.json") as f:
    config = json.load(f)

def monitor(status_var):
    from PIL import Image
    while True:
        img = screen_capture.capture_screen()
        print("[DEBUG] Screenshot captured. Size:", img.size)

        # Show the captured screen (optional: comment out if annoying)
        # img.show()  # Uncomment this line for visual debugging

        text = ocr_engine.extract_text_from_image(img)
        print("[DEBUG] Extracted Text:", text[:100])  # show first 100 chars

        if leak_detector.contains_leak(text):
            print("[DEBUG] Leak Detected in text!")
            status_var.set("Leak Detected!")
            obs_controller.trigger_obs_scene()

        elif nsfw_detector.is_nsfw(img):
            print("[DEBUG] NSFW Detected by model!")
            status_var.set("NSFW Detected!")
            obs_controller.trigger_obs_scene()
        else:
            print("[DEBUG] Clean frame. No issues found.")
            status_var.set("Monitoring...")

        time.sleep(config.get("scan_interval_sec", 3))

def run_gui():
    root = tk.Tk()
    root.title("LeakBlock")

    label = tk.Label(root, text="LeakBlock is running...", font=("Arial", 14))
    label.pack(pady=20)

    status_var = tk.StringVar()
    status_label = tk.Label(root, textvariable=status_var, fg="red", font=("Arial", 12))
    status_label.pack()
    status_var.set("Waiting...")

    def start_monitoring():
        threading.Thread(target=monitor, args=(status_var,), daemon=True).start()
        messagebox.showinfo("LeakBlock", "Monitoring started.")

    btn_start = tk.Button(root, text="Start Monitoring", command=start_monitoring)
    btn_start.pack(pady=10)

    root.mainloop()
