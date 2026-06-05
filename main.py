from functions import *
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Input

class AddNewBook(Screen):

    AUTO_FOCUS = "#input_title"

    BINDINGS = [("escape", "app.pop_screen", "Cancel/Go Back")]

    def compose(self) -> ComposeResult:
        yield Static("--- Add a New Book ---")
        yield Input(placeholder="Type a title and press Enter...", id="input_title")
        yield Input(placeholder="Type number of total pages and press Enter...", id="input_pages", type="integer")
        yield Button("Save Book", id="save_btn", variant="success")
        yield Footer()


    def action_add_book(self):
        title_data = self.query_one("#input_title", Input).value
        pages_data = self.query_one("#input_pages", Input).value
        if title_data == "":
                title_data = "New Book"
        if pages_data == "":
                pages_data = 0

        new_book(title_data, pages_data)

        self.query_one("#input_pages", Input).value = ""
        self.query_one("#input_title", Input).value = ""
        app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            self.action_add_book()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.focus_next()
        #self.action_add_book()


class BookReaderApp(App):

    BINDINGS = [
        ("d", "toggle_dark", "Toggle Dark Mode"), 
        ("q", "quit", "Quit")
    ]

    def compose(self) -> ComposeResult:

        yield Header(show_clock=True)
        yield Static("Welcome to your CLI Library!\n")
        yield Input(placeholder="Type a new book title and press Enter...", id="new_book_input")
        yield Button("Start Reading Session", id="timer_btn", variant="success")
        yield Button("New book", id="new_book_btn", variant="success")
        yield Footer()

    def on_mount(self):
        input = self.query_one("#new_book_input")
        input.styles.display = "none"

    def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "timer_btn":

            self.notify("Timer started! (We will build this next)")
        if event.button.id == "new_book_btn":
            self.push_screen(AddNewBook())


if __name__ == "__main__":
    app = BookReaderApp()
    app.run()
