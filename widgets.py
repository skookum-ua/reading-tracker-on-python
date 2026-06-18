from functions import *
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Input, DataTable, ListView, ListItem, Label
from textual.reactive import reactive
from textual.containers import Center, Vertical, Horizontal, Middle

class Timer(Static):

    def on_mount(self):
        self.time = 0
        self.display_update()
        self.timer = self.set_interval(1.0, self.tick, pause=False)
    
    def tick(self):
        self.time += 1
        self.display_update()
        self.app.session_time = self.time #type: ignore

    def display_update(self):
        min, sec = divmod(self.time, 60)
        hour, min = divmod(min, 60)
        self.update(f"Session Time: {hour:02d}:{min:02d}:{sec:02d}")

    def start_timer(self):
        self.timer.resume()

    def pause_timer(self):
        self.timer.pause()

class BookInList(Vertical):

    def __init__(self, title: str, pages: int, progress: int, **kwargs):
        super().__init__(**kwargs)
        self.book_title = title
        self.book_pages = pages
        self.book_progress = progress
        
    def compose(self) -> ComposeResult:
        yield Label(f"[b]{self.book_title}[/b]", classes="row_title")
        with Horizontal(classes="row_details"):
            yield Label(str(self.book_pages), classes="col_pages")
            yield Label(str(self.book_progress), classes="col_progress")

class BookInfo(Vertical):

    def __init__(self, book , **kwargs):
        super().__init__(**kwargs)
        self.book_title = book['title']
        self.book_pages = book['num_pages']
        self.current_page = book['current_page']
        self.reading_time = book['reading_time']
        self.book_progress = book['percent']
        self.reading_speed = book['reading_speed']
        
    def compose(self) -> ComposeResult:
        yield Label(f"[b]{self.book_title}[/b]", classes="row_title")
        with Horizontal(classes="row_details"):
            yield Label(f"Page: {self.current_page}/{str(self.book_pages)}", classes="col_pages")
            yield Label(f"Completed: {str(self.book_progress)}%", classes="col_progress")
        yield Label(f"Reading time: {str(self.reading_time)}", classes="col_time")
        yield Label(f"Reading speed: {str(self.reading_speed)}", classes="col_speed")
