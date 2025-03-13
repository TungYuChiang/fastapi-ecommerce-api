"""
應用程式配置設定
"""
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 數據庫設定
POSTGRES_USER = os.getenv("POSTGRES_USER", "eadmin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "123456")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ecommerce")
DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}")

# Redis 設定
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# RabbitMQ 設定
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@localhost:5672/")

# 應用程式設定
APP_PORT = int(os.getenv("APP_PORT", "8000"))
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")

# JWT 設定
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION = int(os.getenv("JWT_EXPIRATION", "3600"))  # 默認 1 小時 