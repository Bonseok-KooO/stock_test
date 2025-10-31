print("=== 프로그램 시작 ===")

try:
    print("1. 기본 모듈 import 중...")
    import threading
    import webbrowser
    import os
    import sys
    print("   기본 모듈 import 완료")
    
    print("2. FastAPI 모듈 import 중...")
    from fastapi import FastAPI, Request, HTTPException, Query
    from fastapi.responses import HTMLResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    print("   FastAPI 모듈 import 완료")
    
    print("3. uvicorn 모듈 import 중...")
    import uvicorn
    print("   uvicorn 모듈 import 완료")
    
    print("4. 로컬 모듈 import 중...")
    from core import services
    from config import schemas
    from config.data_manager import (
        get_products,
        get_stores,
        add_product,
        add_store,
        delete_product,
        delete_store,
        get_logs,
    )
    print("   로컬 모듈 import 완료")
    
except Exception as e:
    print(f"모듈 import 중 오류 발생: {e}")
    input("Enter를 눌러 종료하세요...")
    exit(1)

print("5. 유틸리티 함수 정의 중...")
def get_resource_path(relative_path):
    """PyInstaller 실행 시 리소스 경로를 올바르게 반환"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

print("6. FastAPI 앱 생성 중...")
app = FastAPI(title="재고 관리 API")

print("7. 정적 파일 및 템플릿 설정 중...")
try:
    static_path = get_resource_path("static")
    if os.path.exists(static_path):
        app.mount("/static", StaticFiles(directory=static_path), name="static")
        templates = Jinja2Templates(directory=static_path)
        print("   정적 파일 설정 완료")
    else:
        print("   static 폴더가 없음 - 기본 템플릿 사용")
        templates = None
except Exception as e:
    print(f"정적 파일 설정 오류: {e}")
    templates = None

print("8. API 엔드포인트 정의 중...")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """메인 HTML 페이지를 렌더링합니다."""
    if templates:
        products = get_products()
        stores = get_stores()
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "products": products, "stores": stores},
        )
    else:
        return HTMLResponse("<h1>재고 관리 시스템</h1><p>API 서버가 실행 중입니다.</p>")

@app.get("/inventory/{product_id}/{store_id}")
async def get_inventory(product_id: str, store_id: str, user_name: str = Query("")):
    """특정 상품의 특정 매장 재고를 조회합니다."""
    result = await services.get_inventories(product_id, store_id, user_name)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result

@app.post("/inventory/fill")
async def fill_inventory(request: schemas.FillInventoryRequest):
    """재고를 채웁니다."""
    result = await services.fill_inventory(
        request.product_id, request.store_id, request.quantity, request.user_name
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {"message": "재고가 성공적으로 채워졌습니다", "data": result}

@app.get("/inventory/initialize/{store_id}")
async def initialize_store_inventory(store_id: str):
    """매장의 모든 재고를 초기화합니다. ⚠️ 주의: 해당 매장의 모든 재고가 초기화됩니다."""
    result = await services.initialize_store_inventory(store_id)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "message": f"매장 '{store_id}'의 모든 재고가 초기화되었습니다",
        "data": result,
    }

@app.post("/products")
async def add_product_api(request: schemas.AddProductRequest):
    """상품 추가"""
    try:
        add_product(request.product_id, request.product_name, request.user_name)
        return {"message": "상품이 추가되었습니다"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/stores")
async def add_store_api(request: schemas.AddStoreRequest):
    """매장 추가"""
    try:
        add_store(request.store_id, request.store_name, request.user_name)
        return {"message": "매장이 추가되었습니다"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/products/{product_id}")
async def delete_product_api(product_id: str):
    """상품 삭제"""
    try:
        delete_product(product_id)
        return {"message": "상품이 삭제되었습니다"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/stores/{store_id}")
async def delete_store_api(store_id: str):
    """매장 삭제"""
    try:
        delete_store(store_id)
        return {"message": "매장이 삭제되었습니다"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/products")
async def get_products_api():
    """상품 목록 조회"""
    return get_products()

@app.get("/api/stores")
async def get_stores_api():
    """매장 목록 조회"""
    return get_stores()

@app.get("/api/logs")
async def get_logs_api(hours: int = 24):
    """사용 로그 조회"""
    return get_logs(hours)

def run_server():
    """Uvicorn 서버를 실행하는 함수"""
    print("9. 서버를 시작합니다...")
    print("   주소: http://127.0.0.1:8000")
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except Exception as e:
        print(f"서버 시작 중 오류 발생: {e}")
        input("Enter를 눌러 종료하세요...")

if __name__ == "__main__":
    print("10. 메인 실행 시작...")
    
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("11. 서버 스레드가 시작되었습니다.")
    print("12. 브라우저를 열고 있습니다...")

    webbrowser.open("http://127.0.0.1:8000")

    try:
        print("13. 프로그램이 실행 중입니다. 종료하려면 Enter를 누르세요.")
        input()
    except Exception as e:
        print(f"오류 발생: {e}")
        input("Enter를 눌러 종료하세요...")
