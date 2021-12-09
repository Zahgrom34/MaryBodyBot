from aiogram import Dispatcher, executor, types
from connect import dp
from handlers import functions
import handlers

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
