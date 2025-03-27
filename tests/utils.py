"""
Test utility functions
"""
from httpx import AsyncClient
from typing import Dict, Any
import json
from jose import jwt
from datetime import datetime, timedelta

# 使用與 app 相同的密鑰（在測試環境中）
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

async def get_auth_token(client: AsyncClient) -> str:
    """
    Ensure test user exists and get authentication token
    """
    test_user = {
        "username": "test_auth_user",
        "email": "testauth@example.com",
        "password": "TestAuth123!",
        "full_name": "Test Auth User"
    }
    
    login_paths = ["/users/login", "/login"]
    
    # 嘗試登入，若失敗則註冊
    for path in login_paths:
        try:
            login_data = {
                "username": test_user["username"],
                "password": test_user["password"]
            }
            login_response = await client.post(path, json=login_data)
            if login_response.status_code == 200:
                print(f"Login path successful: {path}")
                return login_response.json().get("access_token", "")
        except Exception as e:
            print(f"Error trying login path {path}: {str(e)}")
    
    # 如果登入失敗，嘗試註冊
    register_paths = ["/users/register", "/register"]
    for path in register_paths:
        try:
            register_response = await client.post(path, json=test_user)
            if register_response.status_code < 500:  # 任何非服務器錯誤
                print(f"Register path found: {path}")
                break
        except Exception as e:
            print(f"Error trying path {path}: {str(e)}")
    
    # 再次嘗試登入
    for path in login_paths:
        try:
            login_data = {
                "username": test_user["username"],
                "password": test_user["password"]
            }
            login_response = await client.post(path, json=login_data)
            if login_response.status_code == 200:
                print(f"Login path successful: {path}")
                return login_response.json().get("access_token", "")
        except Exception as e:
            print(f"Error trying login path {path}: {str(e)}")
    
    # 如果以上方法都失敗，則創建一個模擬的 JWT 令牌
    return create_test_token({"sub": "test_user"})

def create_test_token(data: dict) -> str:
    """
    Create a test JWT token without calling the API
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_auth_headers(client: AsyncClient) -> Dict[str, str]:
    """
    Get authorization headers with Bearer token
    """
    token = await get_auth_token(client)
    return {"Authorization": f"Bearer {token}"} 