import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import logging
from datetime import datetime

# Configure logging
log_filename = f"file_organizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(filename=log_filename,
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Store history for undo
last_actions = []

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

# --- Organization Rules ---

def organize_by_type(folder):
    """Organize files by extension into subfolders."""
    actions = []
    for filename in os.listdir(folder):
        src = os.path.join(folder, filename)
        if os.path.isfile(src):
            ext = os.path.splitext(filename)[1].lower().strip(".")
            if not ext:
                ext = "Others"
            dest_folder = os.path.join(folder, ext.upper())
            os.makedirs(dest_folder, exist_ok=True)
            dest = os.path.join(dest_folder, filename)
            shutil.move(src, dest)
            actions.append((dest, src))  # store for undo
            log_output.insert(tk.END, f"Moved: {filename} → {ext.upper()}/\n")
            logging.info(f"Moved: {filename} → {ext.upper()}/")
    return actions

def organize_by_date(folder):
    """Organize files into Year/Month folders based on modified date."""
    actions = []
    for filename in os.listdir(folder):
        src = os.path.join(folder, filename)
        if os.path.isfile(src):
            # use modified time instead of creation time
            mtime = os.path.getmtime(src)
            date = datetime.fromtimestamp(mtime)
            year = str(date.year)
            month = date.strftime("%B")
            dest_folder = os.path.join(folder, year, month)
            os.makedirs(dest_folder, exist_ok=True)
            dest = os.path.join(dest_folder, filename)
            shutil.move(src, dest)
            actions.append((dest, src))
            log_output.insert(tk.END, f"Moved: {filename} → {year}/{month}/\n")
            logging.info(f"Moved: {filename} → {year}/{month}/")
    return actions


def organize_by_size(folder):
    """Organize files by size into Small/Medium/Large."""
    actions = []
    for filename in os.listdir(folder):
        src = os.path.join(folder, filename)
        if os.path.isfile(src):
            size = os.path.getsize(src)
            if size < 1_000_000:  # <1MB
                category = "Small"
            elif size < 100_000_000:  # <100MB
                category = "Medium"
            else:
                category = "Large"
            dest_folder = os.path.join(folder, category)
            os.makedirs(dest_folder, exist_ok=True)
            dest = os.path.join(dest_folder, filename)
            shutil.move(src, dest)
            actions.append((dest, src))
            log_output.insert(tk.END, f"Moved: {filename} → {category}/\n")
            logging.info(f"Moved: {filename} → {category}/")
    return actions

# --- Main Actions ---

def run_organizer():
    folder = folder_var.get()
    if not folder:
        messagebox.showwarning("Warning", "Please select a folder first!")
        return

    log_output.insert(tk.END, f"📂 Organizing folder: {folder}\n")
    logging.info(f"Started organizing folder: {folder}")

    actions = []
    if org_var.get() == "type":
        log_output.insert(tk.END, "➡ Organizing by file type/extension...\n")
        actions = organize_by_type(folder)
    elif org_var.get() == "date":
        log_output.insert(tk.END, "➡ Organizing by creation date...\n")
        actions = organize_by_date(folder)
    elif org_var.get() == "size":
        log_output.insert(tk.END, "➡ Organizing by file size...\n")
        actions = organize_by_size(folder)

    if actions:
        last_actions.clear()
        last_actions.extend(actions)  # save last move set for undo
        log_output.insert(tk.END, "✅ Organizer finished\n\n")
        logging.info("Organizer finished")

def undo_last_action():
    """Undo the last file move operations."""
    if not last_actions:
        messagebox.showinfo("Undo", "Nothing to undo!")
        return

    for moved_file, original_path in reversed(last_actions):
        if os.path.exists(moved_file):
            os.makedirs(os.path.dirname(original_path), exist_ok=True)
            shutil.move(moved_file, original_path)
            log_output.insert(tk.END, f"UNDO: {os.path.basename(moved_file)} → back to {original_path}\n")
            logging.info(f"UNDO: {os.path.basename(moved_file)} → back to {original_path}")

    last_actions.clear()
    log_output.insert(tk.END, "✅ Undo completed\n\n")
    logging.info("Undo completed")

def reset_log():
    log_output.delete(1.0, tk.END)

# --- GUI Setup ---

root = tk.Tk()
root.title("Automated File Organizer")
root.geometry("600x600")

# Title
tk.Label(root, text="Automated File Organizer", font=("Helvetica", 16, "bold")).pack(pady=10)

# Folder selection
folder_frame = tk.Frame(root)
folder_frame.pack(pady=5)
folder_var = tk.StringVar()
tk.Entry(folder_frame, textvariable=folder_var, width=40).pack(side="left", padx=5)
tk.Button(folder_frame, text="Browse", command=select_folder).pack(side="left")

# Organize options
org_var = tk.StringVar(value="type")
org_frame = tk.Frame(root)
org_frame.pack(pady=5)
tk.Label(org_frame, text="Organize By:").pack(anchor="center")
tk.Radiobutton(org_frame, text="File Type / Extension", variable=org_var, value="type").pack(anchor="center")
tk.Radiobutton(org_frame, text="Date Created", variable=org_var, value="date").pack(anchor="center")
tk.Radiobutton(org_frame, text="File Size", variable=org_var, value="size").pack(anchor="center")

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
tk.Button(button_frame, text="Run Organizer", command=run_organizer, width=15).pack(side="left", padx=10)
tk.Button(button_frame, text="Undo", command=undo_last_action, width=15).pack(side="left", padx=10)
tk.Button(button_frame, text="Reset Log", command=reset_log, width=15).pack(side="left", padx=10)
tk.Button(button_frame, text="Exit", command=root.quit, width=15).pack(side="left", padx=10)

# Log output
log_frame = tk.Frame(root)
log_frame.pack(pady=10)
tk.Label(log_frame, text="Log Output:").pack(anchor="center")
log_output = scrolledtext.ScrolledText(log_frame, width=65, height=12)
log_output.pack()

root.mainloop()
