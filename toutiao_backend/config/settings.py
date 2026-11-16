"""集中管理 MySQL 和 Redis 的连接配置。

优先从环境变量读取（可通过 .env 文件提供），未设置时使用开发默认值。
"""
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

# ---------------- MySQL ----------------
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "toutiao")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "123456")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "news_app")
MYSQL_CHARSET = os.getenv("MYSQL_CHARSET", "utf8mb4")

# 密码中的特殊字符需要转义，避免破坏 URL
ASYNC_DATABASE_URL = (
    f"mysql+aiomysql://{MYSQL_USER}:{quote_plus(MYSQL_PASSWORD)}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset={MYSQL_CHARSET}"
)

# ---------------- Redis ----------------
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

# 空字符串按“无密码”处理：redis-py 收到 None 时不会发送 AUTH 命令
# 未设置环境变量时沿用原代码中的密码，避免破坏已有环境
REDIS_PASSWORD = (os.getenv("REDIS_PASSWORD", "Redis@picc364") or "").strip() or None
