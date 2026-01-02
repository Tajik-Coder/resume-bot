import aiosqlite
import asyncio
from config import config
from datetime import datetime

class Database:
    def __init__(self):
        self.db_path = config.DATABASE_PATH
        
    async def create_tables(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    registered_at TEXT,
                    last_activity TEXT
                )
            ''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    message TEXT,
                    created_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            await db.commit()
    
    async def add_user(self, user_id: int, username: str, first_name: str, last_name: str):
        async with aiosqlite.connect(self.db_path) as db:
            current_time = datetime.now().isoformat()
            
            # Check if user exists
            cursor = await db.execute(
                "SELECT * FROM users WHERE user_id = ?",
                (user_id,)
            )
            user = await cursor.fetchone()
            
            if not user:
                await db.execute(
                    "INSERT INTO users (user_id, username, first_name, last_name, registered_at, last_activity) VALUES (?, ?, ?, ?, ?, ?)",
                    (user_id, username, first_name, last_name, current_time, current_time)
                )
            else:
                await db.execute(
                    "UPDATE users SET last_activity = ?, username = ?, first_name = ?, last_name = ? WHERE user_id = ?",
                    (current_time, username, first_name, last_name, user_id)
                )
            await db.commit()
    
    async def add_feedback(self, user_id: int, message: str):
        async with aiosqlite.connect(self.db_path) as db:
            current_time = datetime.now().isoformat()
            await db.execute(
                "INSERT INTO feedback (user_id, message, created_at) VALUES (?, ?, ?)",
                (user_id, message, current_time)
            )
            await db.commit()
    
    async def get_user_stats(self):
        async with aiosqlite.connect(self.db_path) as db:
            # Total users
            cursor = await db.execute("SELECT COUNT(*) FROM users")
            total_users = (await cursor.fetchone())[0]
            
            # Today's active users
            cursor = await db.execute(
                "SELECT COUNT(*) FROM users WHERE date(last_activity) = date('now')"
            )
            active_today = (await cursor.fetchone())[0]
            
            # New users today
            cursor = await db.execute(
                "SELECT COUNT(*) FROM users WHERE date(registered_at) = date('now')"
            )
            new_today = (await cursor.fetchone())[0]
            
            # Total feedback
            cursor = await db.execute("SELECT COUNT(*) FROM feedback")
            total_feedback = (await cursor.fetchone())[0]
            
            return {
                "total_users": total_users,
                "active_today": active_today,
                "new_today": new_today,
                "total_feedback": total_feedback
            }
    
    async def get_all_users(self):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT user_id, username, first_name, last_name, registered_at FROM users ORDER BY registered_at DESC"
            )
            return await cursor.fetchall()

db = Database()