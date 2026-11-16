from fastapi import APIRouter, Depends, HTTPException, status
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest, UserChangePasswordRequest
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import users
from utils.response import success_response
from utils.auth import get_current_user

router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):   # 用户信息 和 db
    # 注册逻辑：验证用户是否存在 --> 创建用户 --> 生成Token --> 响应结果
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="用户已存在")
    user = await users.create_user(db, user_data)
    await db.commit()
    await db.refresh(user)
    token = await users.create_token(db, user.id)
    # return {
    #   "code": 200,
    #   "message": "注册成功",
    #   "data": {
    #     "token": token,
    #     "userInfo": {
    #       "id": user.id,
    #       "username": user.username,
    #       "bio": user.bio,
    #       "avatar": user.avatar}   # avatar: 用户头像
    #   }
    # }
    response_data = UserAuthResponse(token = token, user_info = UserInfoResponse.model_validate( user))
    return success_response(message = "注册成功", data = response_data)

# 用户登录
@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 登录逻辑：验证用户是否存在 --> 验证密码 --> 生成Token --> 响应结果
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token = token, user_info = UserInfoResponse.model_validate( user))
    return success_response(message = "登录成功", data = response_data)


# 查Token用户 --> 封装crud --> 功能整合成一个工具函数 --> 路由导入使用:依赖注入
@router.get("/info")
async def get_user_info(user: users.User = Depends(get_current_user)):
    return success_response(message = "获取用户信息成功", data = UserInfoResponse.model_validate(user))


# 修改用户信息: 验证Token --> 更新（用户输入数据--put-->请求体参数-->定义pydantic模型类）--> 响应结果
# 参数：用户输入数据 + 验证Token的 + db(调用更新方法)
@router.put("/update")
async def update_user_info(user_data: UserUpdateRequest, user: users.User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    updated_user = await users.update_user(db, user.username, user_data)
    return success_response(message = "修改用户信息成功", data = UserInfoResponse.model_validate(updated_user))



# 修改密码（更新）
@router.put("/password")
async def update_password(
        password_data: UserChangePasswordRequest,
        user: users.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):
    res_change_pwd = await users.change_password(db, user, password_data.old_password, password_data.new_password)
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="旧密码错误,修改密码失败")
    return success_response(message = "修改密码成功")



















