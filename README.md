# 头条新闻 — 新闻资讯应用

一个基于 FastAPI + Vue 3 的移动端新闻资讯应用，支持新闻浏览、分类筛选、收藏管理、浏览历史记录和 AI 智能问答功能。

## 技术栈

### 后端
| 技术 | 说明 |
|------|------|
| Python 3.12 | 编程语言 |
| FastAPI | 异步 Web 框架 |
| SQLAlchemy 2.0 | 异步 ORM |
| MySQL 8.0 | 关系型数据库 |
| Redis 7 | 缓存数据库 |
| aiomysql | 异步 MySQL 驱动 |

### 前端
| 技术 | 说明 |
|------|------|
| Vue 3 | 前端框架（Composition API） |
| Vite | 构建工具 |
| Pinia | 状态管理 |
| Vant 4 | 移动端 UI 组件库 |
| Vue Router | 路由管理 |
| Axios | HTTP 请求库 |

## 功能特性

- **用户系统** — 注册、登录、信息修改、密码修改
- **新闻浏览** — 分类筛选、分页列表、新闻详情
- **新闻收藏** — 添加/取消收藏、收藏列表管理
- **浏览历史** — 自动记录浏览历史、单条删除/一键清空
- **AI 问答** — 接入大模型，智能对话功能
- **缓存加速** — Redis 缓存新闻分类和列表数据，提升响应速度

## 快速开始

### 前置条件

- Python 3.12+
- MySQL 8.0
- Redis 7+
- Node.js 18+
- npm 或 yarn

### 1. 初始化数据库

```bash
# 登录 MySQL 并执行 SQL 脚本
mysql -u root -p < toutiao_backend/database.sql
```

执行后会自动创建 `news_app` 数据库，包含用户表、新闻分类表、新闻表、收藏表、浏览历史表等，并插入测试数据。

### 2. 启动后端

```bash
# 进入后端目录
cd toutiao_backend

# 创建虚拟环境（首次）
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Mac / Linux:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload
```

后端启动后访问 http://localhost:8000/docs 可查看 Swagger 接口文档。

> **配置文件说明：**
>
> - `config/db_conf.py` — MySQL 连接地址（默认 `root:123456@localhost:3306/news_app`）
> - `config/cache_conf.py` — Redis 连接地址（默认 `localhost:6379`）
>
> 如果数据库或 Redis 配置不一致，直接修改这两个文件即可。

### 3. 启动前端

```bash
# 进入前端目录
cd toutiao_frontend

# 安装依赖（首次）
npm install

# 启动开发服务器
npm run dev
```

### 4. 访问项目

| 地址 | 说明 |
|------|------|
| http://localhost:5173 | 前端页面（移动端适配） |
| http://localhost:8000/docs | 后端 Swagger 接口文档 |
| http://localhost:8000/redoc | 后端 ReDoc 接口文档 |

## 项目结构

```
toutiao_heima/
│
├── toutiao_backend/                   # 后端项目
│   ├── main.py                        # 应用入口 & 路由注册
│   ├── config/                        # 配置文件
│   │   ├── db_conf.py                 # 数据库连接配置
│   │   └── cache_conf.py              # Redis 连接配置
│   ├── cache/                         # 缓存逻辑
│   │   └── news_cache.py              # 新闻缓存 key 管理
│   ├── crud/                          # 数据库操作层
│   │   ├── news.py                    # 新闻 CRUD（直查数据库）
│   │   ├── news_cache.py              # 新闻 CRUD（缓存优先）
│   │   ├── users.py                   # 用户 CRUD
│   │   ├── favorite.py                # 收藏 CRUD
│   │   └── history.py                 # 历史记录 CRUD
│   ├── models/                        # ORM 模型
│   │   ├── news.py                    # 新闻 & 分类模型
│   │   ├── users.py                   # 用户 & Token 模型
│   │   ├── favorite.py                # 收藏模型
│   │   └── history.py                 # 历史记录模型
│   ├── routers/                       # API 路由
│   │   ├── news.py                    # 新闻接口
│   │   ├── users.py                   # 用户接口
│   │   ├── favorite.py                # 收藏接口
│   │   └── history.py                 # 历史记录接口
│   ├── schemas/                       # Pydantic 数据模型
│   ├── utils/                         # 工具函数
│   │   ├── auth.py                    # Token 鉴权
│   │   ├── security.py                # 密码加密
│   │   ├── response.py                # 统一响应格式
│   │   ├── exception.py               # 异常处理
│   │   └── import_sql.py              # 数据库初始化脚本
│   ├── database.sql                   # 数据库建表 & 测试数据
│   └── requirements.txt               # Python 依赖
│
├── toutiao_frontend/                  # 前端项目
│   ├── index.html
│   ├── vite.config.js                 # Vite 配置
│   ├── package.json                   # 前端依赖
│   └── src/
│       ├── main.js                    # 入口文件
│       ├── App.vue                    # 根组件
│       ├── config/
│       │   └── api.js                 # API 地址 & AI 配置
│       ├── store/                     # Pinia 状态管理
│       │   ├── user.js                # 用户状态
│       │   └── modules/
│       │       ├── news.js            # 新闻状态
│       │       ├── favorite.js        # 收藏状态
│       │       └── history.js         # 历史记录状态
│       ├── views/                     # 页面组件
│       ├── router/                    # 路由配置
│       └── components/                # 公共组件
│
└── README.md                          # 本文件
```

## 测试账号

| 用户名 | 密码 |
|--------|------|
| 小园 | 666666 |

（可在数据库 `user` 表中自行添加更多测试账号）

## API 接口概览

| 模块 | 接口 | 方法 | 说明 |
|------|------|------|------|
| 新闻 | `/api/news/categories` | GET | 获取新闻分类 |
| 新闻 | `/api/news/list` | GET | 获取新闻列表（分页） |
| 新闻 | `/api/news/detail?id=` | GET | 获取新闻详情 |
| 用户 | `/api/user/register` | POST | 用户注册 |
| 用户 | `/api/user/login` | POST | 用户登录 |
| 用户 | `/api/user/info` | GET | 获取用户信息 |
| 用户 | `/api/user/update` | PUT | 修改用户信息 |
| 用户 | `/api/user/password` | PUT | 修改密码 |
| 收藏 | `/api/favorite/check` | GET | 检查收藏状态 |
| 收藏 | `/api/favorite/add` | POST | 添加收藏 |
| 收藏 | `/api/favorite/remove` | DELETE | 取消收藏 |
| 收藏 | `/api/favorite/list` | GET | 收藏列表 |
| 收藏 | `/api/favorite/clear` | DELETE | 清空收藏 |
| 历史 | `/api/history/add` | POST | 添加浏览记录 |
| 历史 | `/api/history/list` | GET | 浏览历史列表 |
| 历史 | `/api/history/delete/:id` | DELETE | 删除单条记录 |
| 历史 | `/api/history/clear` | DELETE | 清空历史记录 |

> 完整接口文档请启动后端后访问 http://localhost:8000/docs

## 注意事项

- 如果 Redis 未启动，项目仍可正常运行，只是缓存功能不可用
- API Key 请勿提交到公开仓库，建议使用环境变量管理
- 本项目为移动端适配，在浏览器中建议使用移动端开发者模式预览
