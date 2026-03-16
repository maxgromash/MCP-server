import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Operations-Department")
BASE_DIR = "/Users/mgrebenshchikov/MCP-server/mcp-facts-server"

@mcp.tool()
async def create_project_ticket(title: str, description: str) -> str:
    """Создает запись о новой задаче (симуляция Jira/Linear)."""
    return f"Тикет [TASK-{hash(title) % 1000}] успешно создан: {title}"

@mcp.tool()
async def export_to_markdown(filename: str, content: str) -> str:
    """Сохраняет финальный отчет в файл .md."""
    path = os.path.join(BASE_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Отчет сохранен локально: {path}"

if __name__ == "__main__":
    mcp.run()