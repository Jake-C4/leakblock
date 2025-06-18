import tkinter as tk
from tkinter import ttk, messagebox
import threading, time
from core import screen_capture, ocr_engine, leak_detector, obs_controller, nsfw_detector
import json

with open("config.json") as f:
    config = json.load(f)

# Shared state
monitoring = False

def monitor(status_var, log_box):
    global monitoring
    while monitoring:
        img = screen_capture.capture_screen()
        text = ocr_engine.extract_text_from_image(img)
        nsfw = nsfw_detector.is_nsfw(img)

        if leak_detector.contains_leak(text):
            status_var.set("Leak Detected!")
            obs_controller.trigger_obs_scene()
            log_box.insert(tk.END, "Leak Detected!\n")

        elif nsfw:
            status_var.set("NSFW Detected!")
            obs_controller.trigger_obs_scene()
            log_box.insert(tk.END, "NSFW Detected!\n")

        else:
            status_var.set("Monitoring...")
            log_box.insert(tk.END, "Clean frame.\n")

        log_box.see(tk.END)  # auto-scroll
        time.sleep(config.get("scan_interval_sec", 3))

def run_gui():
    global monitoring
    root = tk.Tk()
    root.title("LeakBlock")
    root.geometry("600x400")

    tabControl = ttk.Notebook(root)

    dashboard_tab = ttk.Frame(tabControl)
    settings_tab = ttk.Frame(tabControl)
    about_tab = ttk.Frame(tabControl)

    tabControl.add(dashboard_tab, text="Dashboard")
    tabControl.add(settings_tab, text="Settings")
    tabControl.add(about_tab, text="About")
    tabControl.pack(expand=1, fill="both")

    # Dashboard
    status_var = tk.StringVar(value="Idle")
    status_label = tk.Label(dashboard_tab, textvariable=status_var, font=("Arial", 14))
    status_label.pack(pady=10)

    log_box = tk.Text(dashboard_tab, height=12, width=70)
    log_box.pack(pady=10)

    def toggle_monitoring():
        global monitoring
        if not monitoring:
            monitoring = True
            threading.Thread(target=monitor, args=(status_var, log_box), daemon=True).start()
            messagebox.showinfo("LeakBlock", "Monitoring started.")
        else:
            monitoring = False
            status_var.set("Stopped.")
            messagebox.showinfo("LeakBlock", "Monitoring stopped.")

    toggle_btn = tk.Button(dashboard_tab, text="Start/Stop Monitoring", command=toggle_monitoring)
    toggle_btn.pack()

    # Settings (add input fields here later)
    tk.Label(settings_tab, text="Settings coming soon...").pack(pady=20)

    # About
    tk.Label(about_tab, text="LeakBlock v1.0", font=("Arial", 16)).pack(pady=10)
    tk.Label(about_tab, text="Created by Jake\nhttps://github.com/Jake-C4/leakblock").pack()

    root.mainloop()
