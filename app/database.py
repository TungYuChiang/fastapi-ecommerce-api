import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 從環境變數獲取數據庫 URL，如果不存在則使用默認值
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://eadmin:123456@localhost:5432/ecommerce"
)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
