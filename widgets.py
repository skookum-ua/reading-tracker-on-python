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

    def __init__(self, book, **kwargs):
        super().__init__(**kwargs)
        self.book_title = book.get('title')
        self.book_pages = book.get('num_pages')
        self.book_progress = book.get('percent')
        self.book_current_page = book.get('current_page')
        
    def compose(self) -> ComposeResult:
        yield Label(f"[b]{self.book_title}[/b]", classes="row_title")
        with Horizontal(classes="row_details"):
            yield Label(f"Page: {self.book_current_page}/{str(self.book_pages)}", classes="col_pages")
            yield Label(f"{str(self.book_progress)}%", classes="col_progress")

class BookInfo(Vertical):

    def __init__(self, book, **kwargs):
        super().__init__(**kwargs)
        self.book_title = book['title']
        self.book_pages = book['num_pages']
        self.current_page = book['current_page']
        self.reading_time = book['reading_time']
        self.book_progress = book['percent']
        self.reading_speed = book['reading_speed']
        
    def compose(self) -> ComposeResult:
        min, sec = divmod(self.reading_time, 60)
        hour, min = divmod(min, 60)
        min_speed, sec_speed = divmod(self.reading_speed, 60)
        yield Label(f"[b]Selected book:[/b]", classes="row_title")
        yield Label(f"[b]{self.book_title}[/b]", classes="row_title")
        with Horizontal(classes="row_details"):
            yield Label(f"Page: {self.current_page}/{str(self.book_pages)}", classes="col_pages")
            yield Label(f"Completed: {str(self.book_progress)}%", classes="col_progress")
        yield Label(f"Reading time: {hour:02d}h {min:02d}m {sec:02d}s", classes="col_time")
        yield Label(f"Reading speed: {int(min_speed)}m {int(sec_speed)}s /page", classes="col_speed")

class UserInfo(Vertical):

    def __init__(self, booklist, config, **kwargs):
        super().__init__(**kwargs)
        self.booklist = booklist
        self.config = config
        
    def compose(self) -> ComposeResult:

        reading_speed = 0
        num_books = 0
        sessions = self.config['sessions']
        reading_time = self.config['all_reading_time']

        for book in self.booklist.items():
            reading_speed += int(book[1]['reading_speed'])
            num_books += 1
        try:
            reading_speed = reading_speed / num_books
        except:
            reading_speed = 0

        min, sec = divmod(reading_time, 60)
        hour, min = divmod(min, 60)
        min_speed, sec_speed = divmod(reading_speed, 60)
        yield Label(f"[b]User statistics:[/b]", classes="row_title")

        yield Label(f"Total reading time: {hour:02d}h {min:02d}m {sec:02d}s", classes="col_time")
        yield Label(f"Average speed: {int(min_speed)}m {int(sec_speed)}s /page", classes="col_speed")
        yield Label(f"Sessions: {sessions}", classes="col_sessions")
        
