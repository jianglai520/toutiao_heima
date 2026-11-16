from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import users
from starlette import status


# 整合根据 Token查询用户，返回用户
async def get_current_user(
        authorization: str = Header(..., alias = "Authorization"),
        db: AsyncSession = Depends(get_db)):
    # 标准格式: "Bearer XXX"
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的认证格式")
    user = await users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的或者过期的令牌")
    return user
