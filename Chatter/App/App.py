# -*- coding: utf-8 -*-
"""
Create Date: 2023/10/18
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
"""

import os
import secrets
from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from Chatter.Utils.Build import (  # 自定義模組，包含構建和掛載 playground 的函數
    ADMIN_PATH,
    JUDGE_PATH,
    build_and_mount_playground,
)

# 需要身份驗證的路徑列表
AUTH_NEEDED_PATH = [ADMIN_PATH, JUDGE_PATH]

# 創建 FastAPI 實例
app = FastAPI(
    title="Chatter Judge",  # API 標題
    description="Judge with ChatGPT",  # API 描述
    version="Chatter-v0.0.1-beta",  # API 版本
    docs_url="/docs",  # OpenAPI 文檔路徑
)

# 創建靜態文件目錄
os.makedirs("static", exist_ok=True)

# 掛載靜態文件目錄
app.mount(
    "/static",  # 掛載路徑
    StaticFiles(directory="static"),  # 靜態文件目錄
    name="static",  # 掛載名稱
)


# 登錄路由
@app.post("/auth/login")
async def login(
    username: Annotated[str, Form()],  # 表單用户名
    password: Annotated[str, Form()],  # 表單密碼
    request: Request,  # 請求對象
) -> RedirectResponse:
    # TODO: 使用資料庫驗證用户名和密碼
    if username == "admin" and password == "admin":
        request.session["user"] = username  # 將用户名存儲在 Session 中
        return RedirectResponse(url=ADMIN_PATH, status_code=303)  # 重定向到管理頁面
    elif username == "user" and password == "user":
        request.session["user"] = username  # 將用户名存儲在 Session 中
        return RedirectResponse(url=JUDGE_PATH, status_code=303)  # 重定向到評判頁面
    else:
        return RedirectResponse(
            url=f"/?error=Invalid username or password", status_code=303
        )  # 重定向到登錄頁面並顯示錯誤信息


# 登出路由
@app.get("/auth/logout")
async def logout(request: Request) -> RedirectResponse:
    request.session.clear()  # 清除 Session 數據
    return RedirectResponse(url="/", status_code=303)  # 重定向到首頁


# 構建和掛載 playground
app = build_and_mount_playground(app)


# 身份驗證中介軟體
@app.middleware("http")
async def check_auth(request: Request, call_next):
    current_user = request.session.get("user")  # 獲取當前用户信息
    if not current_user and any(
        request.url.path.startswith(path) for path in AUTH_NEEDED_PATH
    ):  # 未登錄且請求路徑需要身份驗證
        return RedirectResponse(url="/", status_code=303)  # 重定向到首頁
    if request.url.path.startswith(ADMIN_PATH) and current_user != "admin":  # 請求管理頁面但不是管理員
        return JSONResponse(status_code=403, content={"message": "Not authorized"})  # 返回 403 錯誤
    return await call_next(request)  # 调用下一個中介軟體或路由


# 添加 Session 中介軟體
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32))  # 使用安全密钥


# Favicon 路由
@app.get("/favicon.ico", include_in_schema=False)  # 不在 OpenAPI 文檔中顯示
async def favicon() -> FileResponse:
    return FileResponse("./static/favicon.ico")  # 返回 Favicon 圖標文件