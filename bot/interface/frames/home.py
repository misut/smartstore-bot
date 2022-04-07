import re
import tkinter
from tkinter import ttk, simpledialog, messagebox

from loguru import logger

from bot.domain import Account, StoreType


class HomeFrame(ttk.Frame):
    master: ttk.Frame

    accounts_combobox: ttk.Combobox
    url_entry: ttk.Entry

    accounts: list[Account] = []

    def __init__(self, master: ttk.Frame) -> None:
        self.master = master

        super().__init__(master=master)
        self.grid(column=0, row=0)
        self.event_info()

        ttk.Label(master=master, text="현재 계정:").grid(column=0, row=0, sticky=tkinter.N+tkinter.W)

        self.accounts_combobox = ttk.Combobox(master=master, values=["+ 계정 추가"], state="readonly", width=20)
        self.accounts_combobox.grid(column=0, row=1, pady=(0, 30), sticky=tkinter.N+tkinter.W)
        self.accounts_combobox.bind("<<ComboboxSelected>>", self.select_account)
        self.accounts_combobox.set("계정을 선택해주세요")

        ttk.Label(master=master, text="상품 URL을 입력해주세요").grid(column=0, row=2, sticky=tkinter.N+tkinter.W)

        self.url_entry = ttk.Entry(master=master, width=60)
        self.url_entry.grid(column=0, row=3, pady=(0, 30), sticky=tkinter.N+tkinter.W)

        ttk.Button(master=master, text="GO", command=self.fetch_product).grid(column=1, row=3, pady=(0, 30))

        ttk.Label(master=master, text="상품 이름:").grid(column=0, row=4, sticky=tkinter.N+tkinter.W)
        ttk.Label(master=master, text="상품 가격:").grid(column=0, row=5, sticky=tkinter.N+tkinter.W)

    def add_account(self, id: str, password: str) -> None:
        account = Account(id=id, password=password)

        self.accounts_combobox["values"] = tuple([account.id]) + self.accounts_combobox["values"]
        self.accounts_combobox.set(account.id)
        logger.debug(f"Account({account.id}) added")

    def select_account(self, *args) -> None:
        if self.accounts_combobox.get() != "+ 계정 추가":
            return
    
        self.accounts_combobox.set("계정을 선택해주세요")

        id = simpledialog.askstring("계정 추가", "ID")
        if id is None:
            return
        
        password = simpledialog.askstring("계정 추가", "Password")
        if password is None:
            return
        
        self.add_account(id, password)
        self.accounts_combobox.set(id)

    def fetch_product(self, *args) -> None:
        url = self.url_entry.get()
        res = re.match("https:\/\/(.+)\.naver\.com\/(.+)\/products\/([0-9]+)", url)
        if not res:
            messagebox.showerror("URL 입력 오류", "URL 제대로 입력하세요!")

        store_type = StoreType(res.groups()[0])
        store_name = res.groups()[1]
        product_id = int(res.groups()[2])

        logger.debug(f"Product(product_name) added")
