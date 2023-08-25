from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from keyboards import keyboards as kb
from database import database as db
from dotenv import load_dotenv
import random
import os
import io
