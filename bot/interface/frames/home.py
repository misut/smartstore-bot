import re
import time
import tkinter
from datetime import datetime, timedelta
from tkinter import messagebox, simpledialog, ttk

from dependency_injector import wiring
from loguru import logger

from bot.domain import (
    Account,
    AccountRepository,
    Product,
    SmartStoreErrander,
    StoreType,
)
from bot.interface.container import Container


@wiring.inject
def get_account(
    id: str,
    accounts: AccountRepository = wiring.Provide[Container.accounts],
) -> Account | None:
    with accounts as repo:
        return repo.get(id)


@wiring.inject
def insert_account(
    account: Account,
    accounts: AccountRepository = wiring.Provide[Container.accounts],
) -> None:
    with accounts as repo:
        repo.insert(account)
        repo.commit()


@wiring.inject
def select_accounts(
    accounts: AccountRepository = wiring.Provide[Container.accounts],
) -> list[Account]:
    with accounts as repo:
        return repo.select()


@wiring.inject
def update_account(
    id: str,
    password: str,
    accounts: AccountRepository = wiring.Provide[Container.accounts],
) -> None:
    with accounts as repo:
        account = repo.get(id)
        account.password = password
        repo.update(account)
        repo.commit()


@wiring.inject
def delete_account(
    id: str,
    accounts: AccountRepository = wiring.Provide[Container.accounts],
) -> None:
    with accounts as repo:
        repo.delete(id)
        repo.commit()


@wiring.inject
def fetch_product(
    product_id: int,
    store_name: str,
    store_type: StoreType = StoreType.SMARTSTORE,
    hidden_errander: SmartStoreErrander = wiring.Provide[Container.hidden_errander],
) -> Product:
    with hidden_errander:
        return hidden_errander.fetch_product(product_id, store_name, store_type)


@wiring.inject
def buy_product(
    account: Account,
    product: Product,
    minutes: int = 0,
    hidden: bool = False,
    errander: SmartStoreErrander = wiring.Provide[Container.errander],
    hidden_errander: SmartStoreErrander = wiring.Provide[Container.hidden_errander],
) -> None:
    selected_errander = hidden_errander if hidden else errander

    started_at = datetime.now()
    with selected_errander:
        selected_errander.login(account)

        while datetime.now() - started_at < timedelta(
            minutes=minutes
        ) and not selected_errander.check_product(product):
            time.sleep(1)

        selected_errander.buy_product(product)


class HomeFrame(ttk.Frame):
    master: ttk.Frame

    accounts_combobox: ttk.Combobox
    url_entry: ttk.Entry
    pname_str: tkinter.StringVar
    price_str: tkinter.StringVar
    minutes_spinbox: ttk.Spinbox

    id: str = ""
    product: Product = None

    def __init__(self, master: ttk.Frame) -> None:
        self.master = master

        super().__init__(master=master)
        self.grid(column=0, row=0)
        self.event_info()

        ttk.Label(master=master, text="?????? ??????:").grid(
            column=0, row=0, sticky=tkinter.N + tkinter.W
        )

        accounts = select_accounts()
        values = [account.id for account in accounts] + ["+ ?????? ??????"]
        self.accounts_combobox = ttk.Combobox(
            master=master, values=values, state="readonly", width=20
        )
        self.accounts_combobox.grid(
            column=0, row=1, pady=(0, 30), sticky=tkinter.N + tkinter.W
        )
        self.accounts_combobox.bind("<<ComboboxSelected>>", self.select_account)
        self.accounts_combobox.set("????????? ??????????????????")

        ttk.Button(master=master, text="?????? ??????", command=self.update_account).grid(
            column=1, row=1, pady=(0, 30), sticky=tkinter.N + tkinter.E
        )

        ttk.Button(master=master, text="?????? ??????", command=self.delete_account).grid(
            column=2, row=1, pady=(0, 30), sticky=tkinter.N + tkinter.E
        )

        ttk.Label(master=master, text="?????? URL??? ??????????????????").grid(
            column=0, row=2, sticky=tkinter.N + tkinter.W
        )

        self.url_entry = ttk.Entry(master=master, width=60)
        self.url_entry.grid(
            column=0, columnspan=2, row=3, pady=(0, 30), sticky=tkinter.N + tkinter.W
        )

        ttk.Button(master=master, text="?????? ????????????", command=self.fetch_product).grid(
            column=2, row=3, pady=(0, 30)
        )

        ttk.Label(master=master, text="?????? ??????:").grid(
            column=0, row=4, sticky=tkinter.N + tkinter.W
        )

        self.pname_str = tkinter.StringVar()
        ttk.Entry(
            master=master, state="readonly", width=30, textvariable=self.pname_str
        ).grid(column=0, row=5, sticky=tkinter.N + tkinter.W)

        ttk.Label(master=master, text="?????? ??????:").grid(
            column=0, row=6, sticky=tkinter.N + tkinter.W
        )

        self.price_str = tkinter.StringVar()
        ttk.Entry(
            master=master, state="readonly", width=30, textvariable=self.price_str
        ).grid(column=0, row=7, pady=(0, 30), sticky=tkinter.N + tkinter.W)

        ttk.Label(master=master, text="?????? ??????(???):").grid(
            column=0, row=8, sticky=tkinter.N + tkinter.W
        )

        self.minutes_spinbox = ttk.Spinbox(master=master, from_=0, to=43200)
        self.minutes_spinbox.set(0)
        self.minutes_spinbox.grid(
            column=0, row=9, pady=(0, 30), sticky=tkinter.N + tkinter.W
        )

        ttk.Button(master=master, text="\n??????!\n", width=40, command=self.start).grid(
            column=1,
            columnspan=2,
            row=8,
            rowspan=2,
            pady=(0, 30),
            sticky=tkinter.N + tkinter.E,
        )

    def insert_account(self, id: str, password: str) -> None:
        account = Account(id=id, password=password)
        insert_account(account)

        self.accounts_combobox["values"] = (
            tuple([account.id]) + self.accounts_combobox["values"]
        )
        self.accounts_combobox.set(account.id)
        logger.debug(f"Account({account.id}) added")

    def select_account(self, *args) -> None:
        if self.accounts_combobox.get() != "+ ?????? ??????":
            self.id = self.accounts_combobox.get()
            return

        self.accounts_combobox.set("????????? ??????????????????")

        id = simpledialog.askstring("?????? ??????", "ID")
        if id is None:
            return

        password = simpledialog.askstring("?????? ??????", "Password")
        if password is None:
            return

        self.insert_account(id, password)
        self.accounts_combobox.set(id)
        self.id = self.accounts_combobox.get()

    def update_account(self, *args) -> None:
        if self.accounts_combobox.get() in ["????????? ??????????????????", "+ ?????? ??????"]:
            messagebox.showerror("?????? ?????? ??????", "????????? ?????? ??????????????? ??????")
            return

        id = self.accounts_combobox.get()
        password = simpledialog.askstring("???????????? ??????", "Password")
        update_account(id, password)
        messagebox.showinfo("?????? ??????", "????????? ??????????????? ???????????? ???????????????.")

    def delete_account(self, *args) -> None:
        if self.accounts_combobox.get() in ["????????? ??????????????????", "+ ?????? ??????"]:
            messagebox.showerror("?????? ?????? ??????", "????????? ?????? ??????????????? ??????")
            return

        if messagebox.askyesno("?????? ??????", "?????? ????????????????"):
            id = self.accounts_combobox.get()
            delete_account(id)
            account_list = list(self.accounts_combobox["values"])
            account_list.remove(id)
            self.accounts_combobox["values"] = tuple(account_list)
            self.accounts_combobox.set("????????? ??????????????????")
            messagebox.showinfo("?????? ??????", "????????? ??????????????? ?????????????????????.")

    def fetch_product(self, *args) -> None:
        url = self.url_entry.get()
        res = re.match("https:\/\/(.+)\.naver\.com\/(.+)\/products\/([0-9]+)", url)
        if not res:
            messagebox.showerror("URL ?????? ??????", "URL ????????? ???????????????!")
            return

        store_type = StoreType(res.groups()[0])
        store_name = res.groups()[1]
        product_id = int(res.groups()[2])

        product = fetch_product(product_id, store_name, store_type)
        self.product = product
        self.pname_str.set(product.name)
        self.price_str.set(str(product.price) + "???")

        logger.debug(f"Product({product.name}) added")

    def start(self, *args) -> None:
        if self.accounts_combobox.get() in ["????????? ??????????????????", "+ ?????? ??????"]:
            messagebox.showerror("?????? ??????", "????????? ?????? ??????????????? ??????")
            return

        if self.product is None:
            messagebox.showerror("?????? ??????", "?????? ????????? ??????????????????!")
            return

        minutes = int(self.minutes_spinbox.get())

        account = get_account(self.id)
        buy_product(account, self.product, minutes)
