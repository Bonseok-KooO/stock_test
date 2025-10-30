import json
import os
import sys
from typing import List, Dict
from datetime import datetime

def get_data_dir():
    """OS별 적절한 애플리케이션 데이터 디렉토리 반환"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 실행 시: OS별 사용자 애플리케이션 데이터 폴더
        if sys.platform == "win32":
            app_data_dir = os.path.join(os.environ.get('APPDATA', ''), 'InventoryManager')
        else:  # macOS, Linux
            app_data_dir = os.path.expanduser("~/Library/Application Support/InventoryManager")
        os.makedirs(app_data_dir, exist_ok=True)
        return app_data_dir
    else:
        # 개발 환경: 프로젝트 루트의 config 디렉토리
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")

# 데이터 파일 경로
data_dir = get_data_dir()
PRODUCTS_FILE = os.path.join(data_dir, "products.json")
STORES_FILE = os.path.join(data_dir, "stores.json")
LOGS_FILE = os.path.join(data_dir, "logs.json")

# 기본 데이터
DEFAULT_PRODUCTS = [
    {
        "id": "4005808801022",
        "name": "니베아크림60ml",
        "is_default": True,
        "added_by": None,
    },
    {
        "id": "3386460023344",
        "name": "랑방 메리미 EDP 50ml",
        "is_default": True,
        "added_by": None,
    },
    {
        "id": "3386460007092",
        "name": "랑방 루머2로즈 EDP 30ml",
        "is_default": True,
        "added_by": None,
    },
    {
        "id": "8801008120750",
        "name": "뉴트로지나 딥클린 클렌징로션 200ml",
        "is_default": True,
        "added_by": None,
    },
    {
        "id": "8801008122631",
        "name": "뉴트로지나 딥 클린 클렌징 오일 200ml",
        "is_default": True,
        "added_by": None,
    },
    {
        "id": "8801008121108",
        "name": "뉴트로지나 딥클린 포밍 클렌저 175g",
        "is_default": True,
        "added_by": None,
    },
    {
        "id": "8809437394506",
        "name": "3CE 타투 립 틴트 4.2g #YAY OR NAY (온)",
        "is_default": True,
        "added_by": None,
    },
    {
        "id": "8809437394513",
        "name": "3CE 타투 립 틴트 4.2g #CANDY JELLY (온)",
        "is_default": True,
        "added_by": None,
    },
]

DEFAULT_STORES = [
    {"id": "DDAA", "name": "플러스점", "is_default": True, "added_by": None},
    {"id": "DB67", "name": "트윈시티점", "is_default": True, "added_by": None},
    {"id": "D578", "name": "타워팰리스점", "is_default": True, "added_by": None},
]


def load_json_file(file_path: str, default_data: List[Dict]) -> List[Dict]:
    """JSON 파일을 로드하거나 기본 데이터로 초기화"""
    if not os.path.exists(file_path):
        save_json_file(file_path, default_data)
        return default_data

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default_data


def save_json_file(file_path: str, data: List[Dict]):
    """JSON 파일 저장"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_products() -> List[Dict]:
    """상품 목록 조회"""
    return load_json_file(PRODUCTS_FILE, DEFAULT_PRODUCTS)


def get_stores() -> List[Dict]:
    """매장 목록 조회"""
    return load_json_file(STORES_FILE, DEFAULT_STORES)


def add_product(product_id: str, product_name: str, user_name: str):
    """상품 추가"""
    products = get_products()

    if any(p["id"] == product_id for p in products):
        raise ValueError("이미 존재하는 상품 코드입니다")

    products.append(
        {
            "id": product_id,
            "name": product_name,
            "is_default": False,
            "added_by": user_name,
        }
    )

    save_json_file(PRODUCTS_FILE, products)


def add_store(store_id: str, store_name: str, user_name: str):
    """매장 추가"""
    stores = get_stores()

    if any(s["id"] == store_id for s in stores):
        raise ValueError("이미 존재하는 매장 코드입니다")

    stores.append(
        {"id": store_id, "name": store_name, "is_default": False, "added_by": user_name}
    )

    save_json_file(STORES_FILE, stores)


def delete_product(product_id: str):
    """상품 삭제 (기본 상품은 삭제 불가)"""
    products = get_products()
    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        raise ValueError("존재하지 않는 상품입니다")

    if product.get("is_default", False):
        raise ValueError("기본 상품은 삭제할 수 없습니다")

    products = [p for p in products if p["id"] != product_id]
    save_json_file(PRODUCTS_FILE, products)


def delete_store(store_id: str):
    """매장 삭제 (기본 매장은 삭제 불가)"""
    stores = get_stores()
    store = next((s for s in stores if s["id"] == store_id), None)

    if not store:
        raise ValueError("존재하지 않는 매장입니다")

    if store.get("is_default", False):
        raise ValueError("기본 매장은 삭제할 수 없습니다")

    stores = [s for s in stores if s["id"] != store_id]
    save_json_file(STORES_FILE, stores)


def add_log(
    action: str,
    user_name: str,
    product_id: str,
    store_id: str,
    result: str,
    details: str = "",
):
    """로그 추가"""
    logs = load_json_file(LOGS_FILE, [])

    products = get_products()
    stores = get_stores()
    product_name = next(
        (p["name"] for p in products if p["id"] == product_id), product_id
    )
    store_name = next((s["name"] for s in stores if s["id"] == store_id), store_id)

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "user_name": user_name,
        "product_id": product_id,
        "product_name": product_name,
        "store_id": store_id,
        "store_name": store_name,
        "result": result,
        "details": details,
    }

    logs.insert(0, log_entry)  # 최신 로그를 맨 앞에

    # 최대 1000개 로그만 유지
    if len(logs) > 1000:
        logs = logs[:1000]

    save_json_file(LOGS_FILE, logs)


def get_logs(hours: int = 24) -> List[Dict]:
    """로그 조회"""
    logs = load_json_file(LOGS_FILE, [])

    # 시간 필터링은 간단히 최근 100개만 반환
    return logs[:100]
