# 電子商務平台 API

這是一個使用 FastAPI 開發的電子商務平台 API，包含商品管理、用戶管理、訂單處理和支付功能。

## 系統架構

- **Web API**: FastAPI 提供 RESTful API
- **數據庫**: PostgreSQL 存儲應用數據
- **消息隊列**: RabbitMQ 處理訂單事件
- **任務處理**: Celery + Redis 處理異步任務

## 前置需求

- Python 3.8+
- PostgreSQL
- Redis
- RabbitMQ

## 安裝依賴

```bash
pip install -r requirements.txt
```

## 環境配置

1. 確保 PostgreSQL 已啟動並創建數據庫:
   ```
   createdb ecommerce
   ```

2. 確保 Redis 服務器已啟動:
   ```
   redis-server
   ```

3. 確保 RabbitMQ 服務器已啟動:
   ```
   rabbitmq-server
   ```

## 數據庫遷移

使用 Alembic 進行數據庫遷移:

```bash
alembic revision --autogenerate -m "Initial"
alembic upgrade head
```

## 啟動服務

### 啟動 Web API 服務器

```bash
uvicorn main:app --reload
```

### 啟動 Celery Worker

```bash
python worker.py
```

### 啟動 RabbitMQ 消息消費者

啟動所有消費者:
```bash
python consumer.py
```

或者啟動特定消費者:
```bash
python consumer.py --queue order_created
python consumer.py --queue payment_processed
```

## 測試 API

### 使用測試腳本

```bash
python test_order_flow.py
```

### 使用 Swagger UI

訪問 Swagger UI 進行交互式測試:
```
http://localhost:8000/docs
```

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

## 擴展建議

1. 加入產品庫存管理
2. 實現完善的用戶身份驗證
3. 添加購物車功能
4. 實現真實的支付網關整合
5. 添加物流追蹤功能 