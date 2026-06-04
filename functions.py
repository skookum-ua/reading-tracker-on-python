import json
from pathlib import Path
import os
from constants import *

def write_booklist (bookpath, booklist):
    if not os.path.isfile(bookpath):
        os.mkdir("books")
    with open(bookpath, "w") as f:
        json.dump(booklist, f)

def read_bookist(bookpath):
    if not os.path.isfile(bookpath):
        raise Exception("no file")
    with open (bookpath, "r") as f:
        return json.load(f)
    
def new_book(name, num_pages, author = None, current_page = 0,):
    new_book = {"title": name, "author": author, "num_pages": num_pages, "current_page": current_page}
    try:
        old_books = read_bookist(BOOKLIST)
        book_id = list(old_books)[-1] + 1
    except:
        old_books = {}
        book_id = 0
    old_books[book_id] = new_book
    write_booklist(BOOKLIST, old_books)
