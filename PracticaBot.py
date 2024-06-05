import aiogram as ag
import aiogram.client.default as agcd
import aiogram.types as agt
import aiogram.enums as age
import aiogram.filters as agf
import asyncio
import re


TOKEN = '6720744119:AAEY3kIF7uDq_OgO5Aviwd4ufrl2BLr4yy4'
bot = ag.Bot(token=TOKEN,
             default=agcd.DefaultBotProperties(parse_mode=age.ParseMode.HTML))
dp = ag.Dispatcher()

states = [
    'Привет, а на какой библиотеке ты написан?',
    'Понял, спасибо, до свидания.',
]

class TextFilter(agf.Filter):
    def __init__(self, state: int) -> None:
        self.my_text = states[state]

    async def __call__(self, message: agt.Message) -> bool:
        return message.text == self.my_text

class RegexFilter(agf.Filter):
    def __init__(self, state: int) -> None:
        self.pattern = states[state]

    async def __call__(self, message: agt.Message) -> bool:
        match = re.match(self.pattern, message.text)
        return match is not None

class CallbackFilter(agf.Filter):
    def __init__(self, callback_data: str) -> None:
        self.my_callback = callback_data

    async def __call__(self, call: agt.CallbackQuery) -> bool:
        return call.data == self.my_callback

@dp.message(agf.Command('start'))
async def start(message: agt.Message):
    button1 = agt.KeyboardButton(text='Привет, а на какой библиотеке ты написан?')
    keyboard = agt.ReplyKeyboardMarkup(keyboard=[[button1]], one_time_keyboard=True, resize_keyboard=True)
    await message.answer('Привет, я бот, созданный для 11 пратики по ОЦГ', reply_markup=keyboard)

@dp.message(TextFilter(0))
async def reply_first(message: agt.Message):
    button1 = agt.InlineKeyboardButton(text='Спасибо', callback_data='greets')
    keyboard = agt.InlineKeyboardMarkup(inline_keyboard=[[button1]])
    await message.answer('Я написан на библиотеке aiogram.', reply_markup=keyboard)

@dp.callback_query(CallbackFilter('greets'))
async def greeting(call: agt.CallbackQuery):
    button1 = agt.InlineKeyboardButton(text='Кем ты разработан?', callback_data='developers')
    keyboard = agt.InlineKeyboardMarkup(inline_keyboard=[[button1]])
    await call.message.answer('И тебе спасибо за проявленный интерес!', reply_markup=keyboard)

@dp.callback_query(CallbackFilter('developers'))
async def get_devops(call: agt.CallbackQuery):
    button1 = agt.KeyboardButton(text='Понял, спасибо, до свидания.')
    keyboard = agt.ReplyKeyboardMarkup(keyboard=[[button1]], one_time_keyboard=True, resize_keyboard=True)
    await call.message.answer('Я разработан студентами: '
                              '\n<b>Тыщенко Светлана</b> Б9123-01.03.02ии2, '
                              '\n<b>Головко Вадим</b> Б9123-01.03.02ии1', reply_markup=keyboard)

@dp.message(TextFilter(1))
async def bye(message: agt.Message):
    await message.answer('До свидания!')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

