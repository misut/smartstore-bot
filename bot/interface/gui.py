import re
import time
import tkinter
from datetime import datetime, timedelta
from tkinter import ttk

from loguru import logger

from bot.domain import StoreType
from bot.interface import frames
from bot.interface.container import Container
from bot.interface.frames import HomeFrame


class GUI(tkinter.Tk):
    container: Container

    current_frame: ttk.Frame
    main_frame: ttk.Frame

    entry: ttk.Entry
    spinbox: ttk.Spinbox

    def __init__(self) -> None:
        self.container = Container()
        self.container.wire(packages=[frames])
        database = self.container.database()
        database.create_all()

        super().__init__()
        self.geometry("800x400+100+100")
        self.resizable(False, False)

        self.main_frame = ttk.Frame(master=self, padding=10)
        self.main_frame.pack()

        self.current_frame = HomeFrame(master=self.main_frame)
