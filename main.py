import configparser

import dotenv
import six
from dependency_injector import errors, wiring

from bot.interface import GUI

if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()
