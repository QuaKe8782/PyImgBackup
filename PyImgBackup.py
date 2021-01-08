import tkinter as tk
from tkinter.filedialog import askdirectory
import os
from pathlib import Path
import shutil
import json
from tkinter import ttk
import tkinter.messagebox

homedir = str(Path.home())
if not os.path.exists("settings.json"):
    settings = open("settings.json", 'x')
    json_data = {"directory": f"{homedir}\Pictures\PyImgBackup", "backup_photos": "True", "backup_videos": "False", "search_directory": "Downloads, Pictures, Videos"}
    settings = open("settings.json", 'w')
    settings.write(json.dumps(json_data, indent=4))
    settings.close()

with open('settings.json') as file:
    data = json.load(file)
    with open("settings.json", 'w') as settings:
        settings.write(json.dumps(data, indent=4))
        settings.close()
    file.close()

window = tk.Tk()
window.title("PyImgBackup")
window.geometry("640x320")

backup_dir = tk.StringVar(window)
backup_dir.set(data["directory"])

options = [
    "Downloads, Pictures, Videos",
    "All directories",
    "Pictures",
    "Downloads",
    "Videos",
    "Desktop"
    ]

user_choice = tk.StringVar(window)
user_choice.set(data["search_directory"])

def backup_files():
    inject_json()
    if not user_choice.get() in options and not os.path.exists(user_choice.get()):
        error_label.place(x=20, y=240)
        return
    else:
        error_label.place_forget()
    backup = backup_dir.get()
    img_files = []
    vid_files = []
    img_file_formats = ['png', 'jpg', 'jpeg', 'gif', 'heif', 'bmp', 'webp', 'svg']
    vid_file_formats = ['mov', 'mkv', 'webm', 'mp4', 'wmv', 'avi', 'swf', 'flv', 'f4v', 'avchd', 'mpeg']
    directories = []
    if user_choice.get() == "All directories":
        directories = [homedir]
    elif user_choice.get() == "Downloads, Pictures, Videos":
        directories = [f"{homedir}\Downloads", f"{homedir}\Pictures", f"{homedir}\Videos"]
    elif user_choice.get() in options:
        directories = [f"{homedir}\\{user_choice.get()}"]
    else:
        directories = [user_choice.get()]
    copy_dir = []
    
    for directory in directories:
        for root, subdirectories, files in os.walk(directory):
            for file in files:
                if file.split('.')[-1] in img_file_formats:
                    img_files.append((os.path.join(root, file), file))
                elif file.split('.')[-1] in vid_file_formats:
                    vid_files.append((os.path.join(root, file), file))
    
    if not os.path.exists(f"{backup}\PyImgBackup"):
        os.mkdir(f"{backup}\PyImgBackup")
    if not os.path.exists(f"{backup}\PyImgBackup\Image Backups"):
        os.mkdir(f"{backup}\PyImgBackup\Image Backups")
    if not os.path.exists(f"{backup}\PyImgBackup/Video Backups"):
        os.mkdir(f"{backup}\PyImgBackup\Video Backups")
    
    duplicate_files = 0
    files_copied = 0
    if backup_videos.get() is True:
        for file in img_files:
            try:
                shutil.copy(file[0], f"{backup}\PyImgBackup\Image Backups\\{file[1]}")
                files_copied += 1
            except (shutil.SameFileError, PermissionError):
                duplicate_files += 1
                pass
    if backup_videos.get() is True:
        for file in vid_files:
            try:
                shutil.copy(file[0], f"{backup}\PyImgBackup\Video Backups\\{file[1]}")
                files_copied += 1
            except (shutil.SameFileError, PermissionError):
                duplicate_files += 1
                pass
    tkinter.messagebox.showinfo("Backup Complete", f"{files_copied} files copied.")

title = tk.Label(text="PyImgBackup")
title.config(font=("TkDefaultFont", 30))
title.pack()
backup_dir_label = tk.Label(text=f"Backup folder: {backup_dir.get()}")
backup_dir_label.config(font=("TkDefaultFont", 10))
backup_dir_label.place(x=20, y=145)

dropdown_menu_label = tk.Label(text=f"Search directories:")
dropdown_menu_label.place(x=20, y=220)

error_label = tk.Label(text=f"Please enter a valid option.", foreground="red")

go_button = tk.Button(window, text="Go", borderwidth=1, relief=tk.SOLID, command=backup_files, cursor="hand2", width=8)
go_button.place(x=300, y=280)


dropdown_menu = ttk.Combobox(window, width=30, textvariable=user_choice)
dropdown_menu['values'] = options
dropdown_menu.place(x=125, y=220)


backup_photos = tk.BooleanVar()
backup_videos = tk.BooleanVar()


if data["backup_photos"] == "True":
    backup_photos.set(bool(True))
if data["backup_videos"] == "True":
    backup_videos.set(bool(True))


def inject_json():
    with open("settings.json", 'w') as settings:
        data = {"directory": backup_dir.get(), "backup_photos": str(backup_photos.get()), "backup_videos": str(backup_videos.get()), "search_directory": user_choice.get()}
        settings.write(json.dumps(data, indent=4))
        settings.close()


def change_backup_dir():
    buffer = askdirectory()
    if buffer == '':
        return
    backup_dir.set(buffer)
    inject_json()
    backup_dir_label.config(text=f"Backup folder: {backup_dir.get()}")

browse_button = tk.Button(window, text="Browse...", borderwidth=1, relief=tk.SOLID, command=change_backup_dir, cursor="hand2", width=8)
browse_button.place(x=22, y=170)


def update_window():
    inject_json()
    if backup_videos.get() == False and backup_photos.get() == False:
        go_button.place_forget()
    else:
        go_button.place(x=300, y=280)


backup_photos_checkbox = tk.Checkbutton(window, text='Backup photos', variable=backup_photos, onvalue=True, offvalue=False, command=update_window)
backup_photos_checkbox.place(x=20, y=75)
backup_videos_checkbox = tk.Checkbutton(window, text='Backup videos', variable=backup_videos, onvalue=True, offvalue=False, command=update_window)
backup_videos_checkbox.place(x=20, y=100)


window.mainloop()