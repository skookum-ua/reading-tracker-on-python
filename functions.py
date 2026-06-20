import json
import os
from pathlib import Path
from constants import *
from datetime import datetime, timezone

def check_json_files(path):
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f: 
            json.dump({}, f)

def write_json (bookpath, booklist):
    if not os.path.isfile(bookpath):
        os.makedirs(os.path.dirname(bookpath), exist_ok=True)
    with open(bookpath, "w") as f:
        json.dump(booklist, f)

def read_json(bookpath):
    if not os.path.isfile(bookpath):
        raise Exception("no file")
    with open (bookpath, "r") as f:
        return json.load(f)
    

def create_config(path):
    config = {'ordered_books': [], 'sessions': 0, 'all_reading_time': 0}
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        write_json(CONFIG, config)

def new_book(name, num_pages, author = None, current_page = 0,):
    new_book = {"title": name, "author": author, "num_pages": num_pages, "current_page": current_page, "reading_time": 0, "reading_speed": 0, "percent": 0,}
    try:
        old_books = read_json(BOOKLIST)
        book_id = int(list(old_books)[-1]) + 1
    except:
        old_books = {}
        book_id = 0
    old_books[book_id] = new_book
    write_json(BOOKLIST, old_books)
    return book_id