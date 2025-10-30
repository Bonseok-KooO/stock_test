import httpx
import os
from dotenv import load_dotenv
from config.schemas import InventoryPayload
from config.data_manager import add_log

load_dotenv()

CATALOG_BASE_URL = os.getenv("CATALOG_BASE_URL", "http://catalog.oymall-aws-dev.local")
FIXED_QUANTITIES = (100, 100)


async def get_inventories(product_id: str, store_id: str, user_name: str = ""):
    """특정 상품의 특정 매장 재고 정보를 조회합니다."""
    url = f"{CATALOG_BASE_URL}/api/inventories/v1/product/{product_id}"
    params = {}
    if user_name:
        params["user_name"] = user_name

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

            from config.schemas import InventoryApiResponse

            api_response = InventoryApiResponse(**response.json())

            store = next(
                (s for s in api_response.data.stores if s.storeId == store_id), None
            )

            if not store:
                error_msg = f"매장 '{store_id}'에 해당 재고가 없습니다."
                if user_name:
                    add_log(
                        "check", user_name, product_id, store_id, "error", error_msg
                    )
                return {"error": error_msg}

            result = {
                "productId": product_id,
                "storeId": store_id,
                "remainQuantity": store.remainQuantity,
                "stockedInQuantity": store.stockedInQuantity,
            }

            if user_name:
                add_log(
                    "check",
                    user_name,
                    product_id,
                    store_id,
                    "success",
                    f"재고: {store.remainQuantity}",
                )

            return result

    except httpx.HTTPStatusError as e:
        error_msg = f"API 서버 오류 ({e.response.status_code}): {e.response.text}"
        if user_name:
            add_log("check", user_name, product_id, store_id, "error", error_msg)
        return {"error": error_msg}
    except httpx.RequestError as e:
        error_msg = f"네트워크 연결 오류: {str(e)}"
        if user_name:
            add_log("check", user_name, product_id, store_id, "error", error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"재고 조회 실패: {str(e)}"
        if user_name:
            add_log("check", user_name, product_id, store_id, "error", error_msg)
        return {"error": error_msg}


async def fill_inventory(
    product_id: str, store_id: str, quantity: int = None, user_name: str = ""
) -> dict:
    """재고를 채웁니다."""
    url = f"{CATALOG_BASE_URL}/api/inventories/v1/qa/save"

    if quantity is None:
        remain_quantity, stocked_in_quantity = FIXED_QUANTITIES
    else:
        remain_quantity = quantity
        stocked_in_quantity = quantity

    payload = InventoryPayload(
        productId=product_id,
        remainQuantity=remain_quantity,
        stockedInQuantity=stocked_in_quantity,
        storeId=store_id,
    )

    params = {}
    if user_name:
        params["user_name"] = user_name

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url, json=payload.dict(), params=params, timeout=10.0
            )
            response.raise_for_status()
            result = response.json()

            if user_name:
                add_log(
                    "fill",
                    user_name,
                    product_id,
                    store_id,
                    "success",
                    f"재고 설정: {remain_quantity}",
                )

            return result
        except httpx.HTTPStatusError as e:
            error_msg = f"API 서버 오류 ({e.response.status_code}): {e.response.text}"
            if user_name:
                add_log("fill", user_name, product_id, store_id, "error", error_msg)
            return {"error": error_msg}
        except httpx.RequestError as e:
            error_msg = f"네트워크 연결 오류: {str(e)}"
            if user_name:
                add_log("fill", user_name, product_id, store_id, "error", error_msg)
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"재고 채우기 실패: {str(e)}"
            if user_name:
                add_log("fill", user_name, product_id, store_id, "error", error_msg)
            return {"error": error_msg}


async def initialize_store_inventory(store_id: str) -> dict:
    """매장의 모든 재고를 초기화합니다."""
    url = f"{CATALOG_BASE_URL}/api/inventories/v1/verification/initialize/{store_id}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"API 서버 오류 ({e.response.status_code}): {e.response.text}"
            }
        except httpx.RequestError as e:
            return {"error": f"네트워크 연결 오류: {str(e)}"}
        except Exception as e:
            return {"error": f"매장 재고 초기화 실패: {str(e)}"}
