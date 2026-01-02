from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging

from keyboards.builders import main_menu, back_to_menu, cancel_feedback
from database.db import db
from config import config

router = Router()

class FeedbackForm(StatesGroup):
    message = State()

@router.message(Command("start"))
async def cmd_start(message: Message):
    # Register user in database
    await db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    welcome_text = (
        "👋 Привет! Я — интерактивное резюме и портфолио.\n\n"
        "Здесь вы можете узнать о моих навыках, проектах и связаться со мной.\n"
        "Выберите опцию из меню ниже:"
    )
    
    await message.answer(welcome_text, reply_markup=main_menu())

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id != config.ADMIN_ID:
        await message.answer("⛔ У вас нет доступа к этой команде.")
        return
    
    stats = await db.get_user_stats()
    admin_text = (
        "📊 **Панель администратора**\n\n"
        f"👥 Всего пользователей: {stats['total_users']}\n"
        f"📈 Активных сегодня: {stats['active_today']}\n"
        f"🆕 Новых сегодня: {stats['new_today']}\n"
        f"💬 Всего отзывов: {stats['total_feedback']}"
    )
    
    await message.answer(admin_text)

# Tech Stack Handler
@router.callback_query(F.data == "tech_stack")
async def tech_stack(callback: CallbackQuery):
    tech_text = (
       "💻 Мой инженерный арсенал (Year 1 Student)\n\n"
"Backend Development:\n"
"• Python 3.12+: Глубокое понимание asyncio, генераторов, декораторов и контекстных менеджеров.\n"
"• aiogram 3.x: Использование Middlewares, FSM, Custom Filters и Router-based архитектуры.\n"
"• FastAPI: Создание асинхронных API с использованием Pydantic для валидации данных.\n\n"
"Data Storage & Management:\n"
"• PostgreSQL & SQLite: Проектирование реляционных схем, оптимизация запросов и использование aiosqlite / SQLAlchemy.\n"
"• Redis: Интеграция для кэширования состояний FSM и хранения временных данных.\n\n"
"Architecture & Engineering:\n"
"• Clean Architecture: Разделение бизнес-логики, сервисного слоя и интерфейса.\n"
"• SOLID & DRY: Написание поддерживаемого, тестируемого и чистого кода.\n"
"• Dependency Injection: Реализация DI для гибкого управления компонентами приложения.\n\n"
"DevOps & Tools:\n"
"• Docker & Docker Compose: Контейнеризация приложений для стабильного развертывания.\n"
"• Git: Профессиональное владение (branching, merging, pull requests).\n"
"• Linux/Bash: Базовое администрирование серверов для деплоя ботов.\n\n"
"AI & Integrations:\n"
"• Работа с Large Language Models (LLM) через API и провайдеров G4F.\n\n"
"⭐ Моя цель — не просто писать код, а создавать масштабируемые и отказоустойчивые системы."
    )
    
    await callback.message.edit_text(tech_text, reply_markup=back_to_menu())
    await callback.answer()

# Projects Handler
@router.callback_query(F.data == "projects")
async def projects(callback: CallbackQuery):
    projects_text = (
         "📂 Мои проекты\n\n"
    "1. AI Assistant Bot (интеграция с ChatGPT)\n"
    "• Описание: Интеллектуальный бот, который с использованием API OpenAI отвечает на вопросы и помогает в решении различных задач.\n"
    "• Технологии: Python, aiogram, OpenAI API, Aiohttp.\n"
    "• 🔗 Проверить: @RealGPT5_bot\n\n"
    "2. Text-to-Speech (TTS) Converter\n"
    "• Описание: Бот для преобразования введённого текста в аудиофайлы с различными голосами.\n"
    "• Технологии: Python, aiogram, gTTS (или Edge-TTS), многопоточность (multithreading).\n"
    "• 🔗 Проверить: @tts_tajik_bot\n\n"
    "Все боты работают на постоянном сервере и готовы к тестированию.\n"
    "Больше проектов и исходный код доступны на GitHub."
    )
    
    await callback.message.edit_text(projects_text, reply_markup=back_to_menu())
    await callback.answer()

# Get CV Handler
@router.callback_query(F.data == "get_cv")
async def get_cv(callback: CallbackQuery):
    try:
        with open(config.RESUME_PATH, 'rb') as file:
            await callback.message.answer_document(
                document=file,
                caption="📄 Вот мое резюме в формате PDF",
                reply_markup=back_to_menu()
            )
    except FileNotFoundError:
        await callback.message.edit_text(
            "❌ Файл резюме временно недоступен.",
            reply_markup=back_to_menu()
        )
    await callback.answer()

# Contact Me Handler - Start FSM
@router.callback_query(F.data == "contact_me")
async def contact_me(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📝 Пожалуйста, напишите ваше сообщение. "
        "Я получу его и свяжусь с вами в ближайшее время.\n\n"
        "Для отмены нажмите кнопку ниже:",
        reply_markup=cancel_feedback()
    )
    await state.set_state(FeedbackForm.message)
    await callback.answer()

# Feedback Form Handler
@router.message(FeedbackForm.message)
async def process_feedback(message: Message, state: FSMContext):
    # Save feedback to database
    await db.add_feedback(message.from_user.id, message.text)
    
    # Forward to admin
    feedback_text = (
        f"📩 **Новое сообщение от пользователя:**\n\n"
        f"👤 **Пользователь:** {message.from_user.full_name}\n"
        f"🆔 **ID:** {message.from_user.id}\n"
        f"👤 **Username:** @{message.from_user.username}\n\n"
        f"💬 **Сообщение:**\n{message.text}"
    )
    
    try:
        await message.bot.send_message(config.ADMIN_ID, feedback_text)
        await message.answer(
            "✅ Ваше сообщение отправлено! Я свяжусь с вами в ближайшее время.",
            reply_markup=back_to_menu()
        )
    except Exception as e:
        logging.error(f"Failed to send feedback to admin: {e}")
        await message.answer(
            "❌ Произошла ошибка при отправке сообщения. Пожалуйста, попробуйте позже.",
            reply_markup=back_to_menu()
        )
    
    await state.clear()

# Cancel Feedback
@router.callback_query(F.data == "cancel_feedback")
async def cancel_feedback_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "❌ Отправка сообщения отменена.",
        reply_markup=back_to_menu()
    )
    await callback.answer()

# Main Menu Handler
@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    welcome_text = (
        "👋 Снова в главном меню!\n\n"
        "Выберите опцию из меню ниже:"
    )
    await callback.message.edit_text(welcome_text, reply_markup=main_menu())
    await callback.answer()