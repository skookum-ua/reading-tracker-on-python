import json
import os
from pathlib import Path
from constants import *
from datetime import datetime, timezone

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

def update_book (book_id, field, data):
    old_books = read_json(BOOKLIST)
    old_books[book_id][field] = data
    write_json(BOOKLIST, old_books)

def new_session(book_id):
    start_time = datetime.now(timezone.utc)

def save_config(current_book_id,):
    pass