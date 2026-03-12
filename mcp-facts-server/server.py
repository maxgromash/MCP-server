import asyncio
import aiosqlite
import time
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Advanced-Scheduler-Server")
DB_PATH = "/Users/mgrebenshchikov/MCP-server/mcp-facts-server/mcp_data.db"

_initialized = False

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS periodic_data (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
        await db.execute("CREATE TABLE IF NOT EXISTS reminders (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, due_time REAL)")
        await db.commit()

async def background_collector():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
                if response.status_code == 200:
                    fact = response.json().get("text")
                    async with aiosqlite.connect(DB_PATH) as db:
                        await db.execute("INSERT INTO periodic_data (content) VALUES (?)", (fact,))
                        await db.commit()
        except Exception:
            pass
        await asyncio.sleep(15) # Ускорили для теста до 15 сек

async def ensure_initialized():
    global _initialized
    if not _initialized:
        await init_db()
        asyncio.create_task(background_collector())
        _initialized = True

# --- НОВЫЙ ИНСТРУМЕНТ: ОЧИСТКА ---
@mcp.tool()
async def clear_database() -> str:
    """Полностью удаляет все собранные факты и напоминания."""
    await ensure_initialized()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM periodic_data")
        await db.execute("DELETE FROM reminders")
        await db.commit()
    return "База данных успешно очищена. Шедулер начнет собирать данные заново."

@mcp.tool()
async def add_reminder(text: str, delay_seconds: int) -> str:
    await ensure_initialized()
    due_time = time.time() + delay_seconds
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO reminders (text, due_time) VALUES (?, ?)", (text, due_time))
        await db.commit()
    return f"Записал: '{text}'."

@mcp.tool()
async def get_summary() -> str:
    await ensure_initialized()
    async with aiosqlite.connect(DB_PATH) as db:
        # Считаем общее кол-во, чтобы видеть рост
        async with db.execute("SELECT COUNT(*) FROM periodic_data") as c:
            total_facts = (await c.fetchone())[0]

        async with db.execute("SELECT content FROM periodic_data ORDER BY id DESC LIMIT 5") as c:
            facts = await c.fetchall()

        # Показываем и старые, и новые напоминания (последние 5)
        async with db.execute("SELECT text FROM reminders ORDER BY id DESC LIMIT 5") as c:
            reminders = await c.fetchall()

    res = [f"### СТАТИСТИКА АГЕНТА (Всего в базе: {total_facts}) ###\n"]
    res.append("📋 **Последние 5 фактов:**")
    res.extend([f"- {f[0]}" for f in facts] if facts else ["- Данных пока нет"])

    res.append("\n⏰ **Последние напоминания:**")
    res.extend([f"- {r[0]}" for r in reminders] if reminders else ["- Пусто"])

    return "\n".join(res)

if __name__ == "__main__":
    mcp.run()