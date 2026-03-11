from mcp.server.fastmcp import FastMCP
import httpx

# 1. Инициализируем сервер под названием "Facts-Server"
mcp = FastMCP("Facts-Server")

# 2. Регистрируем инструмент.
# Описание (docstring) важно — по нему нейросеть поймет, зачем этот инструмент нужен.
@mcp.tool()
async def get_random_fact() -> str:
    """
    Возвращает случайный бесполезный, но интересный факт.
    """
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"

    async with httpx.AsyncClient() as client:
        # Делаем запрос к публичному API
        response = await client.get(url)
        # Если всё успешно, возвращаем текст факта
        if response.status_code == 200:
            data = response.json()
            return data.get("text", "Не удалось найти факт.")
        else:
            return f"Ошибка API: {response.status_code}"

# 3. Запуск сервера
if __name__ == "__main__":
    mcp.run()