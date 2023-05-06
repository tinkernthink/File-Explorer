import os
import sqlite3
import schedule
import time
from tkinter import *


def create_database():
    conn = sqlite3.connect("file_explorer_cache.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL UNIQUE
        )
    """)

    conn.commit()
    conn.close()


def index_files():
    conn = sqlite3.connect("file_explorer_cache.db")
    cursor = conn.cursor()

    for root, _, files in os.walk('C:\\'):
        for file in files:
            path = os.path.join(root, file)
            try:
                cursor.execute("INSERT INTO file_cache (path) VALUES (?)", (path,))
            except sqlite3.IntegrityError:
                pass

    conn.commit()
    conn.close()


def daily_indexing():
    print("Starting daily indexing...")
    index_files()
    print("Daily indexing completed.")


def search_files(search_query):
    conn = sqlite3.connect("file_explorer_cache.db")
    cursor = conn.cursor()

    cursor.execute("SELECT path FROM file_cache WHERE path LIKE ?", (f"%{search_query}%",))
    results = cursor.fetchall()

    conn.close()
    return [result[0] for result in results]


def on_search():
    search_query = search_var.get()
    results.delete(1.0, END)

    for file_path in search_files(search_query):
        results.insert(INSERT, f"{file_path}\n")


def on_clear():
    search_var.set("")
    results.delete(1.0, END)


create_database()
index_files()

root = Tk()
root.title("File Explorer")

search_var = StringVar()

search_label = Label(root, text="Search:")
search_label.pack()

search_entry = Entry(root, textvariable=search_var)
search_entry.pack()

search_button = Button(root, text="Search", command=on_search)
search_button.pack()

clear_button = Button(root, text="Clear", command=on_clear)
clear_button.pack()

results = Text(root, wrap=WORD)
results.pack(expand=YES, fill=BOTH)

schedule.every().day.at("02:00").do(daily_indexing)

while True:
    schedule.run_pending()
    root.update()
    time.sleep(1)
