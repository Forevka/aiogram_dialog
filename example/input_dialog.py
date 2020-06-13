import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State
from aiogram.types import Message
from abc import ABCMeta, abstractmethod
from aiogram_dialog import Dialog, DataStep
from aiogram_dialog import Field

API_TOKEN = 'BOT TOKEN HERE'

class UserAnswers:
    name = Field[str]('name')
    biggerThanEighteen = Field[str]('biggerThanEighteen')
    height = Field[int]('height')


async def input_done(m: Message, dialog_data: UserAnswers, *args, **kwargs):
    if dialog_data.biggerThanEighteen == 'yes':
        await m.answer(
            f"Спасибо за вашу анкету, {dialog_data.name}. "
            f"Наверно, тяжело иметь рост {dialog_data.height} после 18 лет")
    else:
        await m.answer(
            f"Спасибо за вашу анкету, {dialog_data.name}. "
            f"Наверно, тяжело иметь рост {dialog_data.name}, когда ещё нет даже 18 лет")


dialog = Dialog[UserAnswers](
    steps={
        State("1"): DataStep(
            prompt="Введите ваше имя",
            field=UserAnswers.name,
        ),
        State("2"): DataStep(
            prompt="Вам уже есть 18 лет?",
            variants=[
                ("Да", "yes"),
                ("Нет", "no")
            ],
            reorder_variants_by=2,
            field=UserAnswers.biggerThanEighteen,
        ),
        State("3"): DataStep(
            prompt="Введите ваш рост",
            error_msg="Ошибка, введите целое число!\n\n",
            type_factory=int,
            field=UserAnswers.height,
        ),
    }
)

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

dialog.add_done_callback(input_done)
dialog.register_handler(dp)
dp.register_message_handler(dialog.start)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
