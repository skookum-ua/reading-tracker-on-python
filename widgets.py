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

