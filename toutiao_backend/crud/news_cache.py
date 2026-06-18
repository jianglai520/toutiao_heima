from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from cache.news_cache import get_cached_categories, set_cached_categories, get_cached_news_list, set_cached_news_list
from config.cache_conf import get_cache, set_cache
from models.news import Category, News
from fastapi.encoders import jsonable_encoder
from schemas.base import NewsItemBase



async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # 先尝试从缓存中获取数据
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()
    # 写入缓存
    if categories:
        categories = jsonable_encoder(categories)
        await set_cached_categories(categories)
    # 返回数据
    return categories

async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    # 先尝试从缓存中获取数据
    # 跳过的数量skip = (页码 -1) * 每页数量  --> 页码 = 跳过的数量 // 每页数量 + 1
    page = skip // limit + 1
    cached_list = await get_cached_news_list(category_id, page, limit)   # 缓存数据 json
    if cached_list:   # 要的是 ORM
        return [News(**item) for item in cached_list]

    # 查询指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    # 写入缓存
    if news_list:
        # 先把 orm 数据转换 字典才能写入缓存
        # news_list = jsonable_encoder(news_list)
        # ORM 转成 Pydantic, 再转为字典
        # by_alias = False 不使用别名，保存python风格，因为redis数据是给后端用的
        news_data = [NewsItemBase.model_validate(item).model_dump(mode = "json", by_alias=False) for item in news_list]
        await set_cached_news_list(category_id, page, limit, news_data)

    return news_list


async def get_news_count(db: AsyncSession, category_id: int):
    # 查询指定分类下的新闻数量
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()   # 只能有一个结果,否则报错

async def get_news_detail(db: AsyncSession, news_id: int):
    # 获取新闻详情
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views = News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    # 数据库的更新操作 --> 检查数据库是否真的命中了数据  --> 命中了返回True
    return result.rowcount > 0

async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    # order_by 排序 --> 浏览量和发布时间排序
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.views.desc(),   # 默认是升序，desc表示降序
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    # 列表推导式：推导出新闻的核心数据，然后再return
    return [{
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
        "relatedNews": related_news
    } for news_detail in related_news]


