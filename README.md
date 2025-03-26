# 電子商務平台 API

這是一個使用 FastAPI 開發的電子商務平台 API，包含商品管理、用戶管理、訂單處理和支付功能。

## 系統架構

- **Web API**: FastAPI 提供 RESTful API
- **數據庫**: PostgreSQL 存儲應用數據
- **消息隊列**: RabbitMQ 處理訂單事件
- **任務處理**: Celery + Redis 處理異步任務
- **測試框架**: Pytest 提供 API 測試覆蓋
- **錯誤處理**: 統一的錯誤處理機制

## 技術堆棧

- **FastAPI**: 高性能 API 框架
- **SQLAlchemy**: ORM 數據庫操作
- **Pydantic**: 數據驗證和序列化
- **Celery**: 分散式任務隊列
- **Redis**: 緩存和 Celery 後端
- **RabbitMQ**: 消息隊列
- **Pytest**: 測試框架
- **Docker & Docker Compose**: 容器化部署

## 使用 Docker 運行 (建議)

### 前置需求

- Docker
- Docker Compose

### 啟動所有服務

```bash
docker-compose up -d
```

這將啟動以下服務:
- PostgreSQL 數據庫
- Redis 服務器
- RabbitMQ 消息隊列
- FastAPI 應用程式
- Celery Worker
- RabbitMQ 消費者

### 查看日誌

```bash
# 查看所有服務的日誌
docker-compose logs -f

# 查看特定服務的日誌
docker-compose logs -f api
docker-compose logs -f celery_worker
docker-compose logs -f rabbitmq_consumer
```

### 停止服務

```bash
docker-compose down
```

### 重建服務

如果您修改了代碼或配置，需要重建服務:

```bash
docker-compose build
docker-compose up -d
```

## 本地開發環境

### 前置需求

- Python 3.8+
- PostgreSQL
- Redis
- RabbitMQ

### 安裝依賴

```bash
pip install -r requirements.txt
```

### 環境配置

1. 創建 `.env` 文件並設置以下環境變數:
   ```
   # 數據庫設定
   POSTGRES_USER=eadmin
   POSTGRES_PASSWORD=123456
   POSTGRES_DB=ecommerce
   DATABASE_URL=postgresql://eadmin:123456@localhost:5432/ecommerce

   # Redis 設定
   REDIS_URL=redis://localhost:6379/0

   # RabbitMQ 設定
   RABBITMQ_USER=guest
   RABBITMQ_PASSWORD=guest
   RABBITMQ_URL=amqp://guest:guest@localhost:5672/

   # 應用程式設定
   APP_PORT=8000
   APP_HOST=0.0.0.0
   
   # JWT 設定
   JWT_SECRET=your-secret-key
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION=3600
   ```

2. 確保 PostgreSQL 已啟動並創建數據庫:
   ```
   createdb ecommerce
   ```

3. 確保 Redis 服務器已啟動:
   ```
   redis-server
   ```

4. 確保 RabbitMQ 服務器已啟動:
   ```
   rabbitmq-server
   ```

## 數據庫初始化

使用統一命令行介面創建表格:

```bash
python run.py create-tables
```

## 啟動服務

### 使用統一命令行介面

啟動所有服務:
```bash
python run.py all
```

或者單獨啟動各個服務:

```bash
# 啟動 API 服務器
python run.py api

# 啟動 Celery Worker
python run.py worker

# 啟動 RabbitMQ 消費者 (所有隊列)
python run.py consumer

# 啟動特定 RabbitMQ 消費者
python run.py consumer --queue order_created
python run.py consumer --queue payment_processed
```

### 直接啟動各個服務

如果需要，也可以直接啟動各個服務:

```bash
# 啟動 API 服務器
python api.py
# 或者使用 uvicorn
uvicorn api:app --reload

# 啟動 Celery Worker
python scripts/worker.py

# 啟動 RabbitMQ 消費者
python scripts/consumer.py --queue all
```

## 測試

### 使用 Docker 環境運行測試

確保 Docker 容器已運行，然後執行：

```bash
./scripts/run_tests.sh
```

### 本地運行測試

```bash
# 運行所有測試
pytest

# 運行特定測試文件
pytest tests/api/test_product_api.py

# 運行特定類型的測試
pytest -m api

# 生成測試覆蓋率報告
pytest --cov=app
```

詳細的測試說明請參考 [測試文檔](tests/README.md)。

## 錯誤處理機制

本專案實現了統一的錯誤處理機制，透過自定義異常類處理各種 API 錯誤情況。所有錯誤響應均採用標準格式：

```json
{
  "success": false,
  "error": {
    "code": "ERR_XXX",
    "message": "錯誤訊息",
    "detail": "詳細信息"
  }
}
```

主要錯誤類型：

- `NotFoundError` (404): 請求的資源不存在
- `ValidationError` (422): 請求數據驗證失敗
- `AuthenticationError` (401): 未認證或認證失敗
- `AuthorizationError` (403): 認證成功但無訪問權限
- `ConflictError` (409): 資源衝突
- `ServerError` (500): 伺服器內部錯誤

## API 端點

### 商品管理

- `GET /products`: 獲取所有商品
- `GET /products/{product_id}`: 獲取特定商品
- `POST /products`: 創建新商品
- `PUT /products/{product_id}`: 更新商品
- `DELETE /products/{product_id}`: 刪除商品

### 用戶管理

- `POST /users`: 創建用戶
- `GET /users/{user_id}`: 獲取用戶資料

### 訂單管理

- `POST /orders`: 創建訂單
- `GET /orders/{order_id}`: 獲取特定訂單
- `GET /orders`: 獲取所有訂單

### 支付處理

- `POST /payments/process`: 處理支付
- `GET /payments/status/{order_id}`: 檢查支付狀態

## 訂單處理流程

1. 客戶創建訂單 (`POST /orders`)
2. 系統發布訂單創建事件到 RabbitMQ
3. 客戶提交支付 (`POST /payments/process`)
4. 系統處理支付並發布支付處理事件到 RabbitMQ
5. Celery Worker 驗證支付狀態
6. 客戶可以查詢訂單狀態 (`GET /orders/{order_id}`)

## 項目結構

```
ecommerce/
├── app/
│   ├── config/          # 配置模組
│   ├── models/          # 數據庫模型
│   ├── routers/         # API 路由
│   ├── schemas/         # Pydantic 模型
│   ├── services/        # 業務邏輯
│   ├── tasks/           # Celery 任務
│   ├── messaging/       # 消息處理
│   ├── __init__.py      # 應用程式包初始化
│   ├── celery_app.py    # Celery 配置
│   ├── errors.py        # 錯誤處理機制
│   └── database.py      # 數據庫連接
├── scripts/             # 腳本和工具
│   ├── worker.py        # Celery Worker 啟動
│   └── run_tests.sh     # 測試執行腳本
├── tests/               # 測試目錄
│   ├── api/             # API 測試
│   ├── conftest.py      # 測試固件
│   └── README.md        # 測試文檔
├── api.py               # API 服務入口點
├── run.py               # 統一命令行介面
├── requirements.txt     # 依賴管理
├── Dockerfile           # Docker 配置
├── docker-compose.yml   # Docker Compose 配置
└── .env                 # 環境變數
```

## 擴展建議

1. 加入產品庫存管理
2. 實現完善的用戶身份驗證
3. 添加購物車功能
4. 實現真實的支付網關整合
5. 添加物流追蹤功能
6. 實現用戶評價和評論系統
7. 添加產品分類和搜索功能 