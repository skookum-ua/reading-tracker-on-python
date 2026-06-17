from functions import *
from widgets import *
from screens import *

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Input, DataTable, ListView, ListItem, Label
from textual.reactive import reactive
from textual.containers import Center, Vertical, Horizontal, Middle


if __name__ == "__main__":
    check_json_files(BOOKLIST)
    check_json_files(CONFIG)
    check_json_files(SESSIONS)
    app = BookReaderApp()
    app.run()
