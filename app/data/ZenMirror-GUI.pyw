import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def get_devices():
    try:
        # Run adb devices to get list
        output = subprocess.check_output(['adb', 'devices'], creationflags=subprocess.CREATE_NO_WINDOW).decode('utf-8')
        lines = output.strip().split('\n')[1:]
        devices = []
        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2 and parts[1] == 'device':
                    devices.append(parts[0])
        return devices
    except Exception as e:
        return []

def connect_device():
    selected = listbox.get(tk.ACTIVE)
    if not selected or selected == "No devices found":
        messagebox.showerror("Error", "Please select a valid device")
        return
    
    device_id = selected.split(' ')[0]
    
    # Run ZenMirror with the selected serial
    try:
        subprocess.Popen(['ZenMirror.exe', '-s', device_id], creationflags=subprocess.CREATE_NO_WINDOW)
    except FileNotFoundError:
        messagebox.showerror("Error", "ZenMirror.exe not found! Make sure you are running this from the extracted folder.")

def refresh():
    listbox.delete(0, tk.END)
    devices = get_devices()
    if not devices:
        listbox.insert(tk.END, "No devices found")
    else:
        for d in devices:
            listbox.insert(tk.END, f"{d} (Ready)")

# Setup UI
root = tk.Tk()
root.title("ZenMirror Launcher")
root.geometry("350x250")
root.configure(bg='#1e1e2e') # Dark theme background

# Center the window
root.eval('tk::PlaceWindow . center')

tk.Label(root, text="Select Device to Mirror:", bg='#1e1e2e', fg='#cdd6f4', font=('Segoe UI', 12, 'bold')).pack(pady=15)

# Listbox for devices
listbox = tk.Listbox(root, width=35, height=5, bg='#313244', fg='#cdd6f4', font=('Consolas', 10), selectbackground='#89b4fa', selectforeground='#1e1e2e', borderwidth=0, highlightthickness=1)
listbox.pack(pady=5)

btn_frame = tk.Frame(root, bg='#1e1e2e')
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Refresh", command=refresh, bg='#f38ba8', fg='#11111b', font=('Segoe UI', 10, 'bold'), width=10, relief=tk.FLAT).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Connect", command=connect_device, bg='#a6e3a1', fg='#11111b', font=('Segoe UI', 10, 'bold'), width=10, relief=tk.FLAT).pack(side=tk.LEFT, padx=10)

refresh()
root.mainloop()
