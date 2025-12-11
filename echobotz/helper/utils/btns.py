from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class EchoButtons:
    def __init__(self):
        self.buttons = []

    def data_button(self, key, data):
        self.buttons.append(InlineKeyboardButton(text=key, callback_data=data))
        return self

    def url_button(self, key, url):
        self.buttons.append(InlineKeyboardButton(text=key, url=url))
        return self

    def build(self, cols=2):
        menu = [self.buttons[i:i + cols] for i in range(0, len(self.buttons), cols)]
        return InlineKeyboardMarkup(menu)

    def reset(self):
        self.buttons.clear()
