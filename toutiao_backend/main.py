from fastapi import FastAPI
from routers import news, users, favorite, history
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handlers import register_exception_handlers
from contextlib import asynccontextmanager
from config.cache_conf import check_redis_health, close_redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时：检查 Redis 连接
    redis_ok = await check_redis_health()
    if not redis_ok:
        raise Exception("Redis 连接失败")
    yield
    # 关闭时：关闭 Redis 连接
    await close_redis()

app = FastAPI(lifespan=lifespan)

# 注册异常处理器
register_exception_handlers(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 设置允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 真正企业上线不能这样写，否则会有安全漏洞
    allow_credentials=True,  # 允许cookie
    allow_methods=["*"],   # 允许所有方法
    allow_headers=["*"],   # 允许所有header
)

# 挂载路由/注册路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)

