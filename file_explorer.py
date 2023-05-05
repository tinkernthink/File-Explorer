import os
import string
import tkinter as tk
from tkinter import ttk
import threading
import queue

class FileSearch:
    def __init__(self, root):
        self.root = root
        self.root.title("File Search")
        self.root.geometry("800x400")

        self.create_widgets()

        # Set up the queue and update the GUI
        self.update_queue = queue.Queue()
        self.root.after(100, self.update_files_list)

    def create_widgets(self):
        # Create a frame to hold the search entry and buttons
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(side=tk.TOP, pady=10)

        # Create the search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        # Create the search button
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.start_search)
        self.search_button.pack(side=tk.LEFT, padx=5)

        # Create the clear button
        self.clear_button = tk.Button(self.search_frame, text="Clear", command=self.clear_listbox)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Create a listbox to show the file names
        self.files_listbox = tk.Listbox(self.root)
        self.files_listbox.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def start_search(self):
        search_thread = threading.Thread(target=self.search_files)
        search_thread.start()

    def search_files(self):
        search_query = self.search_var.get().lower()
        if search_query:
            for drive in self.get_drives():
                for root, dirs, files in os.walk(drive):
                    for file in files:
                        if search_query in file.lower():
                            file_path = os.path.join(root, file)
                            self.update_queue.put(file_path)
                    for dir in dirs:
                        if search_query in dir.lower():
                            dir_path = os.path.join(root, dir)
                            self.update_queue.put(dir_path)

    def update_files_list(self):
        try:
            while True:
                file_path = self.update_queue.get_nowait()
                self.files_listbox.insert(tk.END, file_path)
        except queue.Empty:
            pass

        self.root.after(100, self.update_files_list)

    def clear_listbox(self):
        self.files_listbox.delete(0, tk.END)

    def get_drives(self):
        # Get the drive letters on the Windows system
        drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
        return drives

if __name__ == "__main__":
    root = tk.Tk()
    FileSearch(root)
    root.mainloop()
