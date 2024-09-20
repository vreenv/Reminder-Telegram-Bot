from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

lang = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='English')],
                                     [KeyboardButton(text='Čeština')]],
                           resize_keyboard=True,
                           input_field_placeholder='Choose...')


reminder_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="10m", callback_data="delay_10min"),
     InlineKeyboardButton(text="30m", callback_data="delay_30min"),
     InlineKeyboardButton(text="1h", callback_data="delay_1hour"),
     InlineKeyboardButton(text="1d", callback_data="delay_1day")],
    [InlineKeyboardButton(text='Delete reminder', callback_data='delete')]])

reminder_buttons_cz = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="10m", callback_data="delay_10min"),
     InlineKeyboardButton(text="30m", callback_data="delay_30min"),
     InlineKeyboardButton(text="1h", callback_data="delay_1hour"),
     InlineKeyboardButton(text="1d", callback_data="delay_1day")],
    [InlineKeyboardButton(text='Smazat připomínku', callback_data='delete')]])

kbs = {'English': reminder_buttons, 'Čeština': reminder_buttons_cz}
