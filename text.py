import time
import random
import pyautogui
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import sys

running = False
paused = False

def human_type(text, total_duration, active_time, typo_chance=0.1, wrong_word_chance=0.05):
    time.sleep(2)  # Delay before typing
    global running, paused
    running = True
    
    time_per_char = (active_time * 60) / len(text)
    words = text.split()
    
    keyboard_layout = {
        'a': 'qwsz', 'b': 'vghn', 'c': 'xdfv', 'd': 'serfcx',
        'e': 'wsdr', 'f': 'drtgvc', 'g': 'ftyhbv', 'h': 'gyujnb',
        'i': 'ujko', 'j': 'hukm', 'k': 'jilm', 'l': 'kop',
        'm': 'njk', 'n': 'bhjm', 'o': 'iklp', 'p': 'ol',
        'q': 'wa', 'r': 'edft', 's': 'wazxde', 't': 'rfgy',
        'u': 'yhji', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc',
        'y': 'tghj', 'z': 'asx', ' ': ' '
    }
    
    for word in words:
        if not running:
            return
        
        while paused:
            time.sleep(0.1)
        
        if random.uniform(0, 1) < wrong_word_chance:
            wrong_word = random.choice(["apple", "table", "running", "cloud", "ocean", "sunshine", "book", "mountain", "guitar", "forest", "bicycle", "city", "river", "piano", "dolphin", "volcano", "keyboard", "butterfly", "moonlight", "starfish", "desert", "airplane", "cup", "whale", "forest", "jungle", "sky", "stone", "bridge", "compass", "lighthouse", "fountain", "camera", "painting", "rocket", "balloon", "sun", "star", "car", "train", "rainbow", "clouds", "lightning", "mountain", "waterfall", "tiger", "elephant", "pyramid", "sailboat", "snow", "forest", "mountain", "ship", "storm", "tree", "river", "carpet", "island", "ocean", "dinosaur", "castle", "moon", "coffee", "chicken", "guitar", "chocolate", "daisy", "petal", "bird", "moon", "puzzle", "ribbon", "jacket", "soccer", "keyboard", "jewel", "octopus", "night", "snowflake", "palm", "sand", "diamond", "light", "electricity", "robot", "window", "sponge", "drum", "sand", "forest", "breeze", "cloud", "violet", "basket", "camera", "lighthouse", "birdhouse", "whistle", "plaza", "zipper", "rock", "ship", "sail", "funnel"])
            pyautogui.write(wrong_word, interval=random.uniform(0.05, time_per_char))
            time.sleep(random.uniform(0.3, 0.6))
            pyautogui.press('backspace', presses=len(wrong_word), interval=0.1)
            time.sleep(random.uniform(0.2, 0.5))
        
        for char in word:
            if random.random() < typo_chance and char in keyboard_layout:
                typo = random.choice(keyboard_layout[char])
                pyautogui.write(typo, interval=random.uniform(0.05, time_per_char))
                time.sleep(random.uniform(0.1, 0.3))
                pyautogui.press('backspace')
                time.sleep(random.uniform(0.1, 0.4))
            
            pyautogui.write(char, interval=random.uniform(0.05, time_per_char))
        
        pyautogui.write(" ", interval=random.uniform(0.05, time_per_char))
        
        if random.random() < 0.15:
            time.sleep(random.uniform(0.5, 1.5))

def start_typing():
    global running
    if running:
        return
    
    text = text_area.get("1.0", tk.END).strip()
    duration = duration_input.get()
    active_time = active_input.get()
    typo_chance = float(typo_input.get())
    wrong_word_chance = float(wrong_word_input.get())
    
    try:
        total_hours, total_minutes = map(int, duration.split(':'))
        total_duration = total_hours * 60 + total_minutes
        active_minutes = int(active_time)
    except ValueError:
        return
    
    text_area.config(state=tk.DISABLED)
    duration_input.config(state=tk.DISABLED)
    active_input.config(state=tk.DISABLED)
    typo_input.config(state=tk.DISABLED)
    wrong_word_input.config(state=tk.DISABLED)
    root.iconify()
    stop_window.deiconify()
    
    typing_thread = Thread(target=human_type, args=(text, total_duration, active_minutes, typo_chance, wrong_word_chance))
    typing_thread.start()

def stop_typing():
    global running
    running = False
    root.destroy()
    sys.exit()

def pause_typing():
    global paused
    paused = not paused
    if paused:
        root.deiconify()
        stop_window.lift()
        text_area.config(state=tk.NORMAL)
        duration_input.config(state=tk.NORMAL)
        active_input.config(state=tk.NORMAL)
        typo_input.config(state=tk.NORMAL)
        wrong_word_input.config(state=tk.NORMAL)
    else:
        text_area.config(state=tk.DISABLED)
        duration_input.config(state=tk.DISABLED)
        active_input.config(state=tk.DISABLED)
        typo_input.config(state=tk.DISABLED)
        wrong_word_input.config(state=tk.DISABLED)
        root.iconify()

# GUI Setup
root = tk.Tk()
root.title("Pranet's typer")
root.geometry("600x600")
root.configure(bg="#f0f0f0")

title_label = tk.Label(root, text="Typing Simulation", font=("Arial", 14, "bold"), bg="#f0f0f0")
title_label.pack(pady=5)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10, font=("Arial", 10))
text_area.pack(pady=5)

tk.Label(root, text="Total Duration (hh:mm):", bg="#f0f0f0").pack()
duration_input = tk.Entry(root, font=("Arial", 10))
duration_input.pack()
duration_input.insert(0, "1:30")

tk.Label(root, text="Active Writing Time (minutes):", bg="#f0f0f0").pack()
active_input = tk.Entry(root, font=("Arial", 10))
active_input.pack()
active_input.insert(0, "60")

tk.Label(root, text="Typo Frequency (0.0 - 1.0):", bg="#f0f0f0").pack()
typo_input = tk.Entry(root, font=("Arial", 10))
typo_input.pack()
typo_input.insert(0, "0.1")

tk.Label(root, text="Wrong Word Frequency (0.0 - 1.0):", bg="#f0f0f0").pack()
wrong_word_input = tk.Entry(root, font=("Arial", 10))
wrong_word_input.pack()
wrong_word_input.insert(0, "0.05")

start_button = tk.Button(root, text="Start Typing", command=start_typing, font=("Arial", 12), bg="#4CAF50", fg="white")
start_button.pack(pady=5)

# Permanent Stop & Pause Buttons
stop_window = tk.Toplevel()
stop_window.title("Stop Button")
stop_window.geometry("250x150")
stop_window.configure(bg="#f0f0f0")
stop_window.attributes('-topmost', True)
stop_window.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable closing
stop_window.withdraw()

tk.Label(stop_window, text="Control Panel", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=5)

stop_button = tk.Button(stop_window, text="FORCE STOP", command=stop_typing, bg="red", fg="white", font=("Arial", 12, "bold"))
stop_button.pack(expand=True, fill=tk.BOTH, pady=5)

pause_button = tk.Button(stop_window, text="PAUSE/RESUME", command=pause_typing, bg="yellow", fg="black", font=("Arial", 12, "bold"))
pause_button.pack(expand=True, fill=tk.BOTH, pady=5)

root.mainloop()

