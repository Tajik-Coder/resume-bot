from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import config

def main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🚀 Технологии", callback_data="tech_stack"),
        InlineKeyboardButton(text="📂 Мои проекты", callback_data="projects")
    )
    
    builder.row(
        InlineKeyboardButton(text="🐙 Мой GitHub", url=config.GITHUB_URL),
        InlineKeyboardButton(text="📄 Получить резюме (PDF)", callback_data="get_cv")
    )
    
    builder.row(
        InlineKeyboardButton(text="📩 Связаться со мной", callback_data="contact_me")
    )
    
    return builder.as_markup()

def back_to_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="main_menu"))
    return builder.as_markup()

def cancel_feedback() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_feedback"))
    return builder.as_markup()