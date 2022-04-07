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

    def intro(self) -> None:
        self.frame.destroy()
        self.frame = ttk.Frame(self, padding=10)
        self.frame.grid()

        ttk.Label(master=self.frame, text="상품 URL을 복사해주세요").grid(column=0, row=0)
        self.entry = ttk.Entry(master=self.frame, width=80)
        self.entry.grid(column=0, row=1)

        ttk.Label(master=self.frame, text="몇 분동안?(0은 한번만 시도)").grid(column=0, row=2)
        self.spinbox = ttk.Spinbox(master=self.frame, from_=0, to=43200)
        self.spinbox.set(0)
        self.spinbox.grid(column=0, row=3)

        ttk.Button(master=self.frame, text="시작", command=self.start).grid(
            column=0, row=4
        )

    def start(self) -> None:
        minutes = int(self.spinbox.get())
        url = self.entry.get()
        logger.info(f"url: {url}")
        res = re.match("https:\/\/(.+)\.naver\.com\/(.+)\/products\/([0-9]+)", url)
        store_type = StoreType(res.groups()[0])
        store_name = res.groups()[1]
        product_id = int(res.groups()[2])

        started_at = datetime.now()
        errander = self.container.errander()
        with errander:
            product = errander.fetch_product(product_id, store_name, store_type)
            logger.info(f"{product.name}: {product.price}")

            if minutes == 0:
                errander.buy_product(product)
                return

            while datetime.now() - started_at < timedelta(minutes=minutes):
                if not errander.check_product(product.id, store_name, store_type):
                    time.sleep(1)
                    continue

                errander.buy_product(product)
                break
