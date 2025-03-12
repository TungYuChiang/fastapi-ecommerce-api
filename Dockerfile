FROM --platform=linux/arm64 python:3.11-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴文件並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY . .

# 暴露 FastAPI 應用程式端口
EXPOSE 8000

# 默認啟動命令 (可被 docker-compose.yml 覆蓋)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 