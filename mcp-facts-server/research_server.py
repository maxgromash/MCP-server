from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Research-Department")

@mcp.tool()
async def fetch_tech_trends(topic: str) -> str:
    """Ищет последние тренды по конкретной технологии."""
    trends = {
        "android": "Android 16 DP1: упор на предиктивный back-gesture и AI-native API.",
        "ai": "Agentic Workflows становятся стандартом вместо простых чат-ботов."
    }
    return trends.get(topic.lower(), f"Тренды для {topic} пока в обработке.")

@mcp.tool()
async def analyze_complexity(text: str) -> str:
    """Оценивает сложность реализации фичи на основе описания."""
    complexity = "High" if len(text) > 50 else "Medium"
    return f"Предварительная оценка сложности: {complexity}. Требуется ревью архитектором."

if __name__ == "__main__":
    mcp.run()