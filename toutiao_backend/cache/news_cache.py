from config.cache_conf import get_json_cache, set_cache
from typing import List, Dict, Any, Optional

# 新闻相关的缓存方法：新闻分类的读取和写入
# key - value
CATEGORY_KEY = "news:categories"
NEW_LIST_PREFIX = "news:list:"


# 获取新闻分类缓存
async def get_cached_categories():
    return await get_json_cache(CATEGORY_KEY)


# 写入新闻分类缓存: 缓存的数据，过期的时间
# 分类，配置： 7200;列表：600；详情：1800；验证码：120 --数据越稳定，缓存越持久
# 避免所有的key同时过期，引起缓存雪崩
async def set_cached_categories(data: List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORY_KEY, data, expire)



# 写入缓存 -- 新闻列表 key = news_list:分类id:页码:每页数量 + 列表数据 + 过期时间
async def set_cached_news_list(category_id: Optional[int], page: int, size: int, news_list: List[Dict[str, Any]], expire: int = 1800):
    # 调用封装的 Redis 方法，存新闻列表到缓存
    category_part = category_id if category_id is not None else "all"
    key = f"{NEW_LIST_PREFIX}{category_part}:{page}:{size}"
    return await set_cache(key, news_list, expire)


# 读取缓存 -- 新闻列表
async def get_cached_news_list(category_id: Optional[int], page: int, size: int):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEW_LIST_PREFIX}{category_part}:{page}:{size}"
    return await get_json_cache(key)





