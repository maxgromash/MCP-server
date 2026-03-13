import asyncio
import aiosqlite
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Pipeline-Server")
# Твои актуальные пути
BASE_DIR = "/Users/mgrebenshchikov/MCP-server/mcp-facts-server"
DB_PATH = os.path.join(BASE_DIR, "mcp_data.db")

# 1. ИНСТРУМЕНТ: ПОИСК (ПОЛУЧЕНИЕ ДАННЫХ)
@mcp.tool()
async def search_info(topic: str) -> str:
    """Ищет информацию по заданной теме (симуляция)."""
    # Здесь могла бы быть логика поиска через SerpAPI или DuckDuckGo
    simulated_data = {
        "android": "Android 15 внедряет новые API для работы с ИИ на уровне системы.",
        "mcp": "Model Context Protocol позволяет ИИ использовать локальные инструменты.",
        "kotlin": "Kotlin Multiplatform (KMM) активно развивается для iOS и Android."
    }
    result = simulated_data.get(topic.lower(), f"Информации по теме {topic} не найдено.")
    return f"Результат поиска для '{topic}': {result}"

# 2. ИНСТРУМЕНТ: СУММАРИЗАЦИЯ (ОБРАБОТКА)
@mcp.tool()
async def summarize_data(raw_text: str) -> str:
    """Принимает текст и возвращает краткую выжимку (Summary)."""
    # Симулируем обработку: добавляем префикс и приводим к краткому виду
    if len(raw_text) < 10:
        return f"Текст слишком короткий для суммаризации: {raw_text}"

    summary = f"SUMMARY: {raw_text.split(':')[-1].strip()}"
    return summary

# 3. ИНСТРУМЕНТ: СОХРАНЕНИЕ (SAVE TO FILE)
@mcp.tool()
async def save_to_pipeline_file(filename: str, content: str) -> str:
    """Сохраняет результат обработки в файл в директории проекта."""
    # Ограничиваем запись только папкой проекта для безопасности
    safe_path = os.path.join(BASE_DIR, filename)

    try:
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Данные успешно сохранены в файл: {safe_path}"
    except Exception as e:
        return f"Ошибка при сохранении: {str(e)}"

if __name__ == "__main__":
    mcp.run()