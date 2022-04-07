import re
import tkinter
from tkinter import ttk, simpledialog, messagebox

from dependency_injector import wiring
from loguru import logger

from bot.domain import Account, StoreType, Product, SmartStoreErrander, AccountRepository
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


@wiring.inject
def fetch_product(
    product_id: int,
    store_name: str,
    store_type: StoreType = StoreType.SMARTSTORE,
    errander: SmartStoreErrander = wiring.Provide[Container.errander],
) -> Product:
    return errander.fetch_product(product_id, store_name, store_type)


class HomeFrame(ttk.Frame):
    master: ttk.Frame

    accounts_combobox: ttk.Combobox
    url_entry: ttk.Entry
    pname_str: tkinter.StringVar
    price_str: tkinter.StringVar

    product: Product = None

    def __init__(self, master: ttk.Frame) -> None:
        self.master = master

        super().__init__(master=master)
        self.grid(column=0, row=0)
        self.event_info()

        ttk.Label(master=master, text="현재 계정:").grid(column=0, row=0, sticky=tkinter.N+tkinter.W)

        accounts = select_accounts()
        values = [account.id for account in accounts] + ["+ 계정 추가"]
        self.accounts_combobox = ttk.Combobox(master=master, values=values, state="readonly", width=20)
        self.accounts_combobox.grid(column=0, row=1, pady=(0, 30), sticky=tkinter.N+tkinter.W)
        self.accounts_combobox.bind("<<ComboboxSelected>>", self.select_account)
        self.accounts_combobox.set("계정을 선택해주세요")

        ttk.Button(master=master, text="계정 수정", command=self.update_account).grid(column=1, row=1, pady=(0, 30), sticky=tkinter.N+tkinter.E)

        ttk.Button(master=master, text="계정 삭제", command=self.delete_account).grid(column=2, row=1, pady=(0, 30), sticky=tkinter.N+tkinter.E)

        ttk.Label(master=master, text="상품 URL을 입력해주세요").grid(column=0, row=2, sticky=tkinter.N+tkinter.W)

        self.url_entry = ttk.Entry(master=master, width=60)
        self.url_entry.grid(column=0, columnspan=2, row=3, pady=(0, 30), sticky=tkinter.N+tkinter.W)

        ttk.Button(master=master, text="상품 불러오기", command=self.fetch_product).grid(column=2, row=3, pady=(0, 30))

        ttk.Label(master=master, text="상품 이름:").grid(column=0, row=4, sticky=tkinter.N+tkinter.W)

        self.pname_str = tkinter.StringVar()
        ttk.Entry(master=master, state="readonly", width=30, textvariable=self.pname_str).grid(column=0, row=5, sticky=tkinter.N+tkinter.W)

        ttk.Label(master=master, text="상품 가격:").grid(column=0, row=6, sticky=tkinter.N+tkinter.W)

        self.price_str = tkinter.StringVar()
        ttk.Entry(master=master, state="readonly", width=30, textvariable=self.price_str).grid(column=0, row=7, sticky=tkinter.N+tkinter.W)

    def insert_account(self, id: str, password: str) -> None:
        account = Account(id=id, password=password)
        insert_account(account)

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
        
        self.insert_account(id, password)
        self.accounts_combobox.set(id)

    def update_account(self, *args) -> None:
        if self.accounts_combobox.get() in ["계정을 선택해주세요", "+ 계정 추가"]:
            messagebox.showerror("계정 수정 오류", "계정을 먼저 선택하세요 ㅡㅡ")
            return

        id = self.accounts_combobox.get()
        password = simpledialog.askstring("비밀번호 변경", "Password")
        update_account(id, password)
        messagebox.showinfo("계정 수정", "계정이 성공적으로 업데이트 되었습니다.")

    def delete_account(self, *args) -> None:
        if self.accounts_combobox.get() in ["계정을 선택해주세요", "+ 계정 추가"]:
            messagebox.showerror("계정 삭제 오류", "계정을 먼저 선택하세요 ㅡㅡ")
            return
        
        if messagebox.askyesno("계정 삭제", "진짜 삭제할거야?"):
            delete_account(self.accounts_combobox.get())
            messagebox.showinfo("계정 삭제", "계정이 성공적으로 삭제되었습니다.")

    def fetch_product(self, *args) -> None:
        url = self.url_entry.get()
        res = re.match("https:\/\/(.+)\.naver\.com\/(.+)\/products\/([0-9]+)", url)
        if not res:
            messagebox.showerror("URL 입력 오류", "URL 제대로 입력하세요!")
            return

        store_type = StoreType(res.groups()[0])
        store_name = res.groups()[1]
        product_id = int(res.groups()[2])

        product = fetch_product(product_id, store_name, store_type)
        self.product = product
        self.pname_str.set(product.name)
        self.price_str.set(str(product.price)+"원")

        logger.debug(f"Product({product.name}) added")
