from aiogram import Router
from aiogram.types import Message
from keyboards.builders import main_menu

router = Router()

@router.message()
async def handle_other_messages(message: Message):
    await message.answer(
        "Пожалуйста, используйте кнопки меню для навигации.",
        reply_markup=main_menu()
    )