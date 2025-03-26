# API 測試框架

本目錄包含電子商務平台 API 的測試框架與測試案例。測試使用 `pytest` 框架，並整合了 FastAPI 的測試工具，提供全面的 API 測試覆蓋。

## 測試架構

測試架構組織如下：

```
tests/
├── __init__.py           # 測試包定義
├── conftest.py           # 測試固件 (Fixtures)
├── api/                  # API 測試目錄
│   ├── __init__.py
│   ├── test_product_api.py  # 產品 API 測試
│   ├── test_user_api.py     # 用戶 API 測試
│   ├── test_order_api.py    # 訂單 API 測試
│   └── test_main.py         # 主應用程式測試
└── README.md             # 本文檔
```

## 測試標記 (Markers)

我們使用以下 pytest 標記來組織測試：

- `api`: API 端點測試
- `unit`: 單元測試
- `integration`: 整合測試
- `slow`: 執行時間較長的測試
- `e2e`: 端到端測試

## 測試固件 (Fixtures)

在 `conftest.py` 中定義了以下常用測試固件：

- `client`: 非同步 HTTP 客戶端，用於測試 API 端點
- `db_session`: 測試資料庫會話
- `product_data`: 測試產品數據
- `user_data`: 測試用戶數據
- `order_data`: 測試訂單數據
- `payment_data`: 測試支付數據

## 運行測試

### 本地運行測試

1. 確保安裝了所有依賴項：

```bash
pip install -r requirements.txt
```

2. 運行所有測試：

```bash
pytest
```

3. 運行特定測試文件：

```bash
pytest tests/api/test_product_api.py
```

4. 運行特定標記的測試：

```bash
pytest -m api
```

5. 生成測試覆蓋率報告：

```bash
pytest --cov=app
```

### 在 Docker 中運行測試

使用以下命令在現有的 Docker 環境中運行測試：

```bash
./scripts/run_tests.sh
```

這將在 `ecommerce-api` 容器中運行所有測試，並顯示詳細測試結果和覆蓋率報告。

## 錯誤處理機制

測試案例利用我們的統一錯誤處理機制，確保 API 返回標準化的錯誤響應。所有 API 錯誤都繼承自 `BaseAPIError` 類，並返回統一格式：

```json
{
  "success": false,
  "error": {
    "code": "ERR_XXX",
    "message": "錯誤訊息",
    "detail": "可選的詳細信息"
  }
}
```

測試案例驗證 API 在各種錯誤情況下是否返回正確的狀態碼和錯誤格式。

## 常見錯誤類型測試

測試套件包含對以下常見錯誤類型的驗證：

- `NotFoundError` (404): 資源不存在
- `ValidationError` (422): 輸入驗證錯誤
- `AuthenticationError` (401): 未認證
- `AuthorizationError` (403): 未授權
- `ConflictError` (409): 資源衝突
- `ServerError` (500): 伺服器內部錯誤

## 新增測試

添加新測試時，請遵循以下步驟：

1. 在適當的測試目錄中創建測試文件 (如 `tests/api/test_new_feature.py`)
2. 為每個測試案例使用 `@pytest.mark.api` 或其他適當的標記
3. 使用 `@pytest.mark.asyncio` 裝飾所有非同步測試函數
4. 使用固件 (fixtures) 提供測試數據和客戶端
5. 斷言 API 回應是否符合預期

## 最佳實踐

- 每個測試案例應該獨立，不依賴其他測試的狀態
- 使用模擬 (mocks) 進行外部依賴的隔離
- 測試案例應覆蓋正常情況和錯誤情況
- 維持高測試覆蓋率，尤其是核心業務邏輯
- 定期運行測試套件，確保系統穩定性 

## 使用 Docker 指令運行測試

除了使用 `run_tests.sh` 腳本外，你也可以直接使用 Docker 指令來運行測試。以下是使用 Docker 運行測試的詳細說明：

### 使用 docker-compose 啟動服務

首先，確保你的開發環境已經啟動：

```bash
# 啟動所有服務
docker-compose up -d
```

### 使用 docker exec 運行測試

#### 運行所有測試

```bash
# 運行所有測試
docker exec ecommerce-api pytest

# 運行所有測試並顯示詳細輸出
docker exec ecommerce-api pytest -v

# 運行所有測試並生成覆蓋率報告
docker exec ecommerce-api pytest --cov=app
```

#### 運行特定目錄或文件的測試

```bash
# 運行所有 API 測試
docker exec ecommerce-api pytest tests/api/ -v

# 運行特定測試文件
docker exec ecommerce-api pytest tests/api/test_product_api.py -v

# 運行多個測試文件
docker exec ecommerce-api pytest tests/api/test_main.py tests/api/test_product_api.py -v
```

#### 運行特定標記的測試

```bash
# 運行所有標記為 'api' 的測試
docker exec ecommerce-api pytest -m api -v

# 運行所有非慢速測試 (不包含標記為 'slow' 的測試)
docker exec ecommerce-api pytest -m "not slow" -v
```

### 文件同步與更新測試

如果你在本地更新了測試文件，可以使用 `docker cp` 命令將更新的文件複製到容器中：

```bash
# 複製單個測試文件到容器
docker cp tests/api/test_product_api.py ecommerce-api:/app/tests/api/

# 複製測試工具函數
docker cp tests/utils.py ecommerce-api:/app/tests/

# 複製整個測試目錄
docker cp tests/ ecommerce-api:/app/
```

注意：如果你在 `docker-compose.yml` 中正確設置了卷掛載，通常不需要手動複製文件，因為本地文件的更改會自動同步到容器。但如果遇到同步問題，可以使用上述命令進行手動同步。

### 處理測試數據庫

如果測試需要一個乾淨的數據庫環境：

```bash
# 重新創建數據庫表 (慎用，會清除現有數據)
docker exec ecommerce-api python scripts/create_tables.py
```

### 查看測試日誌

```bash
# 查看容器日誌以檢查測試輸出
docker logs ecommerce-api

# 實時查看日誌流
docker logs -f ecommerce-api
```

### 排除常見問題

1. **身份驗證問題**：如果測試中遇到身份驗證錯誤，可能需要確保 JWT 密鑰設置正確。
   
2. **端口衝突**：如果遇到端口已被佔用的錯誤，可以修改 `.env` 文件中的端口設置。

3. **路徑問題**：API 測試可能因路徑配置不同而失敗，確保使用正確的路徑格式（某些端點可能需要尾隨斜杠）。

4. **數據同步**：如果卷掛載未正常工作，使用 `docker cp` 命令手動同步文件。

實施這些測試策略，可確保你的 API 在 Docker 容器中能夠被可靠且一致地測試。 