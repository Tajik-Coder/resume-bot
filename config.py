import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    ADMIN_ID: int = int(os.getenv("ADMIN_ID", 0))
    GITHUB_URL: str = os.getenv("GITHUB_URL", "https://github.com/yourusername")
    DATABASE_PATH: str = "database/users.db"
    RESUME_PATH: str = "assets/resume.pdf"  # You need to add your PDF file here

config = Config()