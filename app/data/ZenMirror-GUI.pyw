import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import os

def get_devices():
    try:
        output = subprocess.check_output(['adb', 'devices'], creationflags=subprocess.CREATE_NO_WINDOW).decode('utf-8')
        lines = output.strip().split('\n')[1:]
        return [line.split()[0] for line in lines if line.strip() and len(line.split()) >= 2 and line.split()[1] == 'device']
    except Exception:
        return []

def connect_device():
    selected = listbox.get(tk.ACTIVE)
    if not selected or selected == "No devices found":
        messagebox.showerror("Error", "Please select a valid device")
        return
    
    device_id = selected.split(' ')[0]
    
    # Build the command based on user selections
    cmd = ['ZenMirror.exe', '-s', device_id]
    
    if var_screen_off.get():
        cmd.append('--turn-screen-off')
    if var_stay_awake.get():
        cmd.append('--stay-awake')
    if var_read_only.get():
        cmd.append('--no-control')
    if var_no_audio.get():
        cmd.append('--no-audio')
    
    res = var_resolution.get()
    if res != "Original (Best)":
        # extract number from string like "720p (Fast)"
        max_size = res.split('p')[0]
        cmd.extend(['-m', max_size])
        
    if var_record.get():
        if not record_path.get():
            messagebox.showerror("Error", "Please select a save location for the recording.")
            return
        cmd.extend(['--record', record_path.get()])
    
    try:
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
    except FileNotFoundError:
        messagebox.showerror("Error", "ZenMirror.exe not found! Make sure you run this from the extracted folder.")

def refresh():
    listbox.delete(0, tk.END)
    devices = get_devices()
    if not devices:
        listbox.insert(tk.END, "No devices found")
    else:
        for d in devices:
            listbox.insert(tk.END, f"{d} (Ready)")

def browse_record_path():
    filename = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 Video", "*.mp4"), ("MKV Video", "*.mkv")], title="Save Recording As")
    if filename:
        record_path.set(filename)
        var_record.set(True)

root = tk.Tk()
root.title("ZenMirror - Advanced Dashboard")
root.geometry("450x550")
root.configure(bg='#1e1e2e')

# Define custom styling colors
bg_color = '#1e1e2e'
fg_color = '#cdd6f4'
accent_color = '#89b4fa'

tk.Label(root, text="Select Device to Mirror:", bg=bg_color, fg=fg_color, font=('Segoe UI', 12, 'bold')).pack(pady=(15, 5))
listbox = tk.Listbox(root, width=45, height=4, bg='#313244', fg=fg_color, font=('Consolas', 10), selectbackground=accent_color, selectforeground='#1e1e2e', borderwidth=0, highlightthickness=1)
listbox.pack(pady=5)

# --- Advanced Options Frame ---
options_frame = tk.LabelFrame(root, text=" Advanced Settings ", bg=bg_color, fg=accent_color, font=('Segoe UI', 10, 'bold'), padx=15, pady=10)
options_frame.pack(fill="both", expand="yes", padx=20, pady=10)

var_screen_off = tk.BooleanVar()
var_stay_awake = tk.BooleanVar()
var_read_only = tk.BooleanVar()
var_no_audio = tk.BooleanVar()
var_record = tk.BooleanVar()
var_resolution = tk.StringVar(value="Original (Best)")
record_path = tk.StringVar()

# Checkboxes
def create_checkbutton(parent, text, var):
    cb = tk.Checkbutton(parent, text=text, variable=var, bg=bg_color, fg=fg_color, selectcolor='#313244', activebackground=bg_color, activeforeground=fg_color, font=('Segoe UI', 9))
    cb.pack(fill='x', pady=2, anchor='w')
    return cb

create_checkbutton(options_frame, "Turn Screen Off (Saves phone battery)", var_screen_off)
create_checkbutton(options_frame, "Stay Awake (Prevent phone from sleeping)", var_stay_awake)
create_checkbutton(options_frame, "Read-Only Mode (View only, no touch control)", var_read_only)
create_checkbutton(options_frame, "Disable Audio (Video only)", var_no_audio)

# Resolution Dropdown
res_frame = tk.Frame(options_frame, bg=bg_color)
res_frame.pack(fill='x', pady=10)
tk.Label(res_frame, text="Video Quality:", bg=bg_color, fg=fg_color, font=('Segoe UI', 9)).pack(side=tk.LEFT)
resolutions = ["Original (Best)", "1080p (High)", "720p (Fast)", "480p (Very Fast)"]
res_dropdown = tk.OptionMenu(res_frame, var_resolution, *resolutions)
res_dropdown.config(bg='#313244', fg=fg_color, activebackground=accent_color, activeforeground='#1e1e2e', highlightthickness=0)
res_dropdown.pack(side=tk.LEFT, padx=10)

# Recording Option
rec_frame = tk.Frame(options_frame, bg=bg_color)
rec_frame.pack(fill='x', pady=5)
cb_record = tk.Checkbutton(rec_frame, text="Record Screen to File", variable=var_record, bg=bg_color, fg=fg_color, selectcolor='#313244', activebackground=bg_color, activeforeground=fg_color, font=('Segoe UI', 9))
cb_record.pack(side=tk.LEFT)
tk.Button(rec_frame, text="Browse...", command=browse_record_path, bg='#45475a', fg=fg_color, relief=tk.FLAT, font=('Segoe UI', 8)).pack(side=tk.LEFT, padx=5)

tk.Label(options_frame, textvariable=record_path, bg=bg_color, fg='#a6e3a1', font=('Segoe UI', 8, 'italic'), wraplength=350, justify=tk.LEFT).pack(fill='x', anchor='w')

# --- Buttons ---
btn_frame = tk.Frame(root, bg=bg_color)
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="↻ Refresh Devices", command=refresh, bg='#f38ba8', fg='#11111b', font=('Segoe UI', 10, 'bold'), width=18, relief=tk.FLAT).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="▶ Connect ZenMirror", command=connect_device, bg='#a6e3a1', fg='#11111b', font=('Segoe UI', 10, 'bold'), width=18, relief=tk.FLAT).pack(side=tk.LEFT, padx=10)

refresh()
root.eval('tk::PlaceWindow . center')
root.mainloop()
