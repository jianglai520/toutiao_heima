import json

import redis.asyncio as redis
from typing import Any

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0


# 创建redis的连接对象
redis_client = redis.Redis(
    host = REDIS_HOST,  # Redis服务器主机地址
    port = REDIS_PORT,   # Redis端口号
    db = REDIS_DB,   # Redis 数据库编号，0~15
    decode_responses=True,   # 是否将字节数据解码为字符串
    socket_connect_timeout=5,   # 连接超时，单位秒
    socket_timeout = 5,   # 读取超时，单位秒
    retry_on_timeout = True  # 是否在超时重试
)


# 设置缓存和读取缓存(字符串 和 列表或字典)
# 读取缓存：字符串
async def get_cache(key: str):
    # return await redis_client.get(key)
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None

# 读取：列表或字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None


# 设置缓存 setex(key, expire, value)
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value, (dict, list)):
            # 转字符串再存
            value = json.dumps(value, ensure_ascii=False)   # 中文正常保存
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"设置缓存失败: {e}")
        return False


# 健康检查： 验证 Redis 是否连通
async def check_redis_health():
    try:
        await redis_client.ping()
        print("Redis连接成功")
        return True
    except Exception as e:
        print(f"Redis 连通性检查失败: {e}")
        return False

# 关闭 Redis 连接
async def close_redis():
    try:
        await redis_client.close()
        print("Redis连接已关闭")
    except Exception as e:
        print(f"Redis 关闭失败: {e}")























