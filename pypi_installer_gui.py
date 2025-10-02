import pypi_installer
import tkinter as tk

root = tk.Tk()
root.title("PyPI Installer GUI")
root.geometry("400x300")

untar = True
unzip = True
label = tk.Label(root, text="Type module to install:", font=("Comic Sans MS", 14))
label.pack(pady=10)

entry = tk.Entry(root, width=30, font=("Arial", 12))
entry.pack(pady=10)

output_label = tk.Label(root, text="", font=("Comic Sans MS", 14))
output_label.pack(pady=20)

def install_pkg():
    try:
        user_input = entry.get()
        output_label.config(text="Installing {user_input}...", font=("Arial", 10))
        pypi_installer.download_pypi_sdist(user_input, unzip=True, untar=True)
        output_label.config(text=f"Attempted to install: {user_input}")
    except Exception as e:
        output_label.config(text=f"Error installing package '{user_input}': {e}", font=("Arial", 10))

def on_toggle1():
    global unzip
    unzip = not unzip
    btn1.config(text=f"Unzip: {'On' if unzip else 'Off'}")

def on_toggle2():
    global untar
    untar = not untar
    btn2.config(text=f"Untar: {'On' if untar else 'Off'}")

btn1 = tk.Button(root, text=f"Unzip: {'On' if unzip else 'Off'}", command=on_toggle1, font=("Arial", 12))    
btn1.pack(pady=5)
btn2 = tk.Button(root, text=f"Untar: {'On' if untar else 'Off'}", command=on_toggle2, font=("Arial", 12))
btn2.pack(pady=5)
button = tk.Button(root, text="Install", command=install_pkg, font=("Arial", 12))
button.pack()

root.mainloop()