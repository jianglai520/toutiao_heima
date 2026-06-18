from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
from utils import security
import uuid
from datetime import timedelta, datetime
from fastapi import HTTPException

# 根据用户名来查询数据库
async def get_user_by_username(db: AsyncSession,username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 先密码加密处理 --> add
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)   # 从数据库读回最新的数据
    return user


# 生成Token
async def create_token(db: AsyncSession, user_id: int):
    # 生成token + 设置过期时间 --> 查询数据库当前用户是否有Token --> 有：更新；无：添加
    token = str(uuid.uuid4())
    # timedelta(days=7, hours = 2, minutes = 30, seconds = 10) --> 7天2小时30分10秒
    expires_at = datetime.now()+ timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
    await db.commit()
    return token


# 验证用户
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user



# 根据Token来查询用户:验证 Token --> 查询用户
async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()

    if not db_token or db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# 更新用户信息: update更新 --> 检查是否命中 --> 获取更新后的用户返回
async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    # user_data 是 pydantic类型, 得到字典--> 解包
    # 没有设置值的不更新
    query = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none = True
    ))
    result = await db.execute(query)
    await db.commit()

    # 检查更新
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 获取一下更新后的用户
    updated_user = await get_user_by_username(db, username)
    return updated_user



# 修改密码：验证旧密码 --> 新密码加密 --> 修改密码
async def change_password(
    db: AsyncSession,
    user: User,
    old_password: str,
    new_password: str):
    if not security.verify_password(old_password, user.password):
        return False
    hashed_new_pwd = security.get_hash_password(new_password)
    user.password = hashed_new_pwd
    db.add(user)  # 更新：由sqlalchemy真正接管 User 对象，确保可以 commit
    # 规避session过期或者关闭导致的不能提交的问题
    await db.commit()
    return True























