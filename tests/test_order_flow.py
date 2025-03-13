#!/usr/bin/env python
"""
訂單流程整合測試
"""
import requests
import json
import time
import sys
import os

# 將項目根目錄添加到 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# API基礎URL
BASE_URL = "http://localhost:8000"


def test_create_order():
    """測試創建訂單"""
    print("正在測試創建訂單...")

    # 訂單數據
    order_data = {
        "items": [
            {
                "product_id": 1,  # 假設產品ID為1
                "quantity": 2,
            },
            {
                "product_id": 2,  # 假設產品ID為2
                "quantity": 1,
            },
        ],
        "payment_method": "credit_card",
    }

    # 發送創建訂單請求
    response = requests.post(f"{BASE_URL}/orders/", json=order_data)

    # 檢查響應
    if response.status_code == 201:
        order = response.json()
        print(f"訂單創建成功！訂單號: {order['order_number']}")
        return order
    else:
        print(f"訂單創建失敗: {response.text}")
        return None


def test_process_payment(order_id):
    """測試處理支付"""
    print(f"正在測試處理訂單 {order_id} 的支付...")

    # 支付數據
    payment_data = {"order_id": order_id, "payment_method": "credit_card"}

    # 發送處理支付請求
    response = requests.post(f"{BASE_URL}/payments/process", json=payment_data)

    # 檢查響應
    if response.status_code == 200:
        result = response.json()
        if result["success"]:
            print(f"支付處理成功！交易ID: {result.get('transaction_id')}")
        else:
            print(f"支付處理失敗: {result.get('message')}")
        return result
    else:
        print(f"支付處理請求失敗: {response.text}")
        return None


def test_check_payment_status(order_id):
    """測試檢查支付狀態"""
    print(f"正在檢查訂單 {order_id} 的支付狀態...")

    # 發送檢查支付狀態請求
    response = requests.get(f"{BASE_URL}/payments/status/{order_id}")

    # 檢查響應
    if response.status_code == 200:
        result = response.json()
        print(f"支付狀態: {result.get('status')}")
        return result
    else:
        print(f"檢查支付狀態失敗: {response.text}")
        return None


def test_get_order(order_id):
    """測試獲取訂單詳情"""
    print(f"正在獲取訂單 {order_id} 的詳情...")

    # 發送獲取訂單詳情請求
    response = requests.get(f"{BASE_URL}/orders/{order_id}")

    # 檢查響應
    if response.status_code == 200:
        order = response.json()
        print(f"訂單狀態: {order['status']}")
        return order
    else:
        print(f"獲取訂單詳情失敗: {response.text}")
        return None


def test_order_flow():
    """測試完整訂單流程"""
    # 步驟1: 創建訂單
    order = test_create_order()
    if not order:
        print("無法繼續測試：訂單創建失敗")
        return

    order_id = order["id"]

    # 步驟2: 處理支付
    payment_result = test_process_payment(order_id)
    if not payment_result:
        print("無法繼續測試：支付處理失敗")
        return

    # 步驟3: 等待異步處理
    print("等待異步處理支付...")
    time.sleep(5)

    # 步驟4: 檢查支付狀態
    payment_status = test_check_payment_status(order_id)

    # 步驟5: 獲取訂單詳情
    updated_order = test_get_order(order_id)

    print("\n--- 測試總結 ---")
    print(f"訂單ID: {order_id}")
    if updated_order:
        print(f"最終訂單狀態: {updated_order['status']}")
        print(f"支付狀態: {updated_order['payment_status']}")

    if payment_result and payment_result.get("success"):
        print("訂單支付流程測試完成！")
    else:
        print("訂單支付流程測試完成，但支付未成功。")


if __name__ == "__main__":
    test_order_flow()

# 要運行此測試，執行:
# python tests/test_order_flow.py