from typing import cast
from functions import *
from widgets import *
from collections import deque
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Input, DataTable, ListView, ListItem, Label
from textual.reactive import reactive
from textual.containers import Center, Vertical, Horizontal, Middle

class BookReaderApp(App):

    CSS = CSS_CONST

    session_time = reactive(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_page = 0
        self.all_books = read_json(BOOKLIST)
        self.config = read_json(CONFIG)
        self.all_sessions = ""
        try:
            self.ordered_books = deque(self.config['ordered_books'])
        except:
            self.ordered_books = deque([])
        self.reading_speed = ""
        try:
            self.current_book = self.ordered_books[0]
        except:
            self.current_book = 0
        

    BINDINGS = [
        ("d", "toggle_dark", "Toggle Dark Mode"), 
        ("q", "quit", "Quit")
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            with Vertical(id="left"):
                yield Static("Welcome to your CLI Library!\n", id="title")
                yield UserInfo(id="userinfo", booklist = self.app.all_books, config = self.app.config) #type: ignore
                yield Button("New book", id="new_book_btn", variant="success",classes="button")
            with Vertical(id="middle"):
                if self.current_book != 0:
                    yield BookInfo(id="bookinfo", book = self.app.all_books[str(self.app.current_book)]) #type: ignore
                yield Button("Start Reading", id="timer_btn", variant="success", classes="button")
            yield ListView(id="mylist")  
        yield Footer()

    def refresh_list(self):
        self.all_books = read_json(BOOKLIST)
        my_list = self.query_one("#mylist", ListView)
        my_list.clear()
        for book_id in self.ordered_books:
            book = self.all_books.get(str(book_id))
            if not book:
                continue
            display_text = BookInList(book)
            new_item = ListItem(display_text)
            new_item.book_id = book_id # type: ignore
            my_list.append(new_item)
    
    async def refresh_bookinfo(self):
        try:
            bookinfo = self.query_one("#bookinfo", BookInfo)
            await bookinfo.remove()
        except:
            return
        middle = self.query_one("#middle", Vertical)
        middle.mount(BookInfo(id="bookinfo", book = self.app.all_books[str(self.app.current_book)]), before= 0) #type: ignore

    async def refresh_userinfo(self):
        try:
            userinfo = self.query_one("#userinfo", UserInfo)
            await userinfo.remove()
        except:
            return
        left= self.query_one("#left", Vertical)
        left.mount(UserInfo(id="userinfo", booklist = self.app.all_books, config = self.app.config), before= "#new_book_btn") #type: ignore

    async def on_mount(self):
        self.refresh_list()
        await self.refresh_bookinfo()
        await self.refresh_userinfo()

    async def on_list_view_selected(self, event: ListView.Selected):
        clicked_item = event.item
        book_id = getattr(clicked_item, "book_id", None)
        if book_id != None:
            self.current_book = book_id
            #self.notify(f"You clicked the book with ID: {book_id}")
            await self.refresh_bookinfo()

    def on_button_pressed(self, event: Button.Pressed):

        if event.button.id == "timer_btn":
            if self.ordered_books:
                self.push_screen(AskForPage("Enter starting page", save = False))
            else:
                self.notify("No books. Create new book.")
        if event.button.id == "new_book_btn":
            self.push_screen(AddNewBook())


class AskForPage(Screen):

    def __init__(self, instruction="Enter page", save = True, **kwargs):
        super().__init__(**kwargs)
        self.instruction = instruction
        self.save = save


    BINDINGS = [("escape", "app.pop_screen", "Cancel/Go Back"),
                ("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Static(f"Current book: {self.app.all_books[str(self.app.current_book)]['title']}")#type:ignore
        yield Static(self.instruction)
        yield Input(value=f"{self.app.all_books[str(self.app.current_book)]['current_page']}", placeholder="Type starting page", id="input_st_page", type="integer") #type: ignore
        yield Button("OK", id="ok_btn", variant="success")
        yield Footer()
    
    def action_set_starting_page(self):
        if self.query_one("#input_st_page", Input).value in ["", "-"] or int(self.query_one("#input_st_page", Input).value) > int(self.app.all_books[str(self.app.current_book)]['num_pages']) or int(self.query_one("#input_st_page", Input).value) < 1: #type: ignore
            self.notify("Enter correct page")
        else:
            self.app.current_page = self.query_one("#input_st_page", Input).value # type: ignore
            self.app.all_books[str(self.app.current_book)]['current_page'] = self.app.current_page #type: ignore
            self.query_one("#input_st_page", Input).value = ""
            if not self.save:
                self.app.switch_screen(ActiveSession())
            else:
                self.dismiss()

    def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "ok_btn":
            if not self.save:
                self.action_set_starting_page()
            elif int(self.app.current_page) <= int(self.query_one("#input_st_page", Input).value):
                self.action_set_starting_page()
            else:
                self.notify("Enter correct page")
            
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        if not self.save:
            self.action_set_starting_page()
        elif int(self.app.current_page) <= int(self.query_one("#input_st_page", Input).value):
                self.action_set_starting_page()
        else:
            self.notify("Enter correct page")
        
class ActiveSession(Screen):

    BINDINGS = [("escape", "app.pop_screen", "Cancel/Go Back")]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.starting_page = self.app.current_page #type: ignore
        
    def compose(self) -> ComposeResult:
        yield Static("--- Read Now ---")
        with Middle():
            with Center():
                yield Timer(id="timer")
                yield Static( "Progress estimation: not enough data", id = "progress")
        with Horizontal():

                yield Button("Pause", id="pause_btn", variant="success")
                yield Button("Continue", id="start_btn", variant="success")
                yield Button("Save and Exit", id="end_session_btn", variant="success")
        yield Footer()

    def on_mount(self):
        if self.app.all_books[str(self.app.current_book)]['reading_speed'] != 0:
            self.watch(self.app, "session_time", self.update_label)

        start = self.query_one("#start_btn", Button)
        start.display = False

    def update_label(self, new_time: int):
        progress_label = self.query_one("#progress", Static)
        prog = round(((int(self.app.current_page) + (new_time / 60) / float(self.app.all_books[str(self.app.current_book)]['reading_speed'])) / int(self.app.all_books[str(self.app.current_book)]['num_pages'])) * 100, 2)
        prog = min(prog, 100.0)
        progress_label.update(f"Progress estimation: {prog}%")


    def on_button_pressed(self, event: Button.Pressed):
        pause = self.query_one("#pause_btn", Button)
        start = self.query_one("#start_btn", Button)
        time = self.query_one("#timer", Timer)
        if event.button.id == "start_btn":
            time.start_timer()
            start.display = False
            pause.display = True
        elif event.button.id == "pause_btn":
            time.pause_timer()
            start.display = True
            pause.display = False
        elif event.button.id == "end_session_btn":
            time.pause_timer()
            self.app.push_screen(AskForPage("Enter stop page", True), callback= self.save_and_exit)

    async def save_and_exit(self, result: object = None):
        time = self.query_one("#timer", Timer).time
        self.app.all_books[str(self.app.current_book)]['reading_time'] += time #type: ignore
        if int(self.app.current_page) - int(self.starting_page) > 0: #type: ignore
            self.app.all_books[str(self.app.current_book)]['reading_speed'] = int(time) / (int(self.app.current_page) - int(self.starting_page))  # minutes per page #type: ignore
        else: 
            self.app.all_books[str(self.app.current_book)]['reading_speed'] = 0 #type: ignore
        self.app.all_books[str(self.app.current_book)]['percent'] = round(int(self.app.current_page) / int(self.app.all_books[str(self.app.current_book)]['num_pages']) * 100, 2) #type: ignore
        self.app.ordered_books.remove(self.app.current_book) #type: ignore
        self.app.ordered_books.appendleft(self.app.current_book) #type: ignore
        self.app.config['ordered_books'] = list(self.app.ordered_books) #type: ignore
        try:
            self.app.config['all_reading_time'] += time #type: ignore
        except:
            self.app.config['all_reading_time'] = time  #type: ignore
        try:
            self.app.config['sessions'] += 1 #type: ignore
        except:
            self.app.config['sessions'] = 1 #type: ignore
        write_json(CONFIG, self.app.config) #type: ignore
        write_json(BOOKLIST, self.app.all_books) #type: ignore
        self.app.refresh_list() #type: ignore
        await self.app.refresh_bookinfo() #type: ignore
        await self.app.refresh_userinfo() #type: ignore
        self.app.pop_screen()
            
class AddNewBook(Screen):

    AUTO_FOCUS = "#input_title"

    BINDINGS = [("escape", "app.pop_screen", "Cancel/Go Back"),
                ("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Static("--- Add a New Book ---")
        yield Input(placeholder="Type a title and press Enter...", id="input_title")
        yield Input(placeholder="Type number of total pages and press Enter...", id="input_pages", type="integer")
        yield Button("Save Book", id="save_btn", variant="success")
        yield Footer()


    async def action_add_book(self):
        title_data = self.query_one("#input_title", Input).value
        pages_data = int(self.query_one("#input_pages", Input).value)
        if title_data == "":
                title_data = "New Book"
        if pages_data == "":
                pages_data = 0

        new_book_id = new_book(title_data, pages_data)
        self.app.all_books = read_json(BOOKLIST) #type: ignore
        self.app.ordered_books.appendleft(new_book_id) #type: ignore
        self.app.config['ordered_books'] = list(self.app.ordered_books) #type: ignore
        write_json(CONFIG, self.app.config) #type: ignore


        self.query_one("#input_pages", Input).value = ""
        self.query_one("#input_title", Input).value = ""
        self.app.refresh_list() #type: ignore
        await self.app.refresh_bookinfo() # type: ignore
        self.app.pop_screen()
        

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            await self.action_add_book()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.focus_next()
        #self.action_add_book()
    