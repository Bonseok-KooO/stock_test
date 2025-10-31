print("=== 프로그램 시작 ===")

try:
    print("1. 기본 모듈 import 중...")
    import threading
    import webbrowser
    import os
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

print("5. FastAPI 앱 생성 중...")
app = FastAPI(title="재고 관리 시스템", version="1.0.0")

print("6. 정적 파일 및 템플릿 설정 중...")
try:
    import os
    if os.path.exists("static"):
        app.mount("/static", StaticFiles(directory="static"), name="static")
        templates = Jinja2Templates(directory="static")
        print("   정적 파일 설정 완료")
    else:
        print("   static 폴더가 없음 - 기본 템플릿 사용")
        templates = None
except Exception as e:
    print(f"정적 파일 설정 오류: {e}")
    templates = None

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/products")
async def get_products_api():
    return get_products()

@app.get("/api/stores")
async def get_stores_api():
    return get_stores()

@app.post("/api/products")
async def add_product_api(product: schemas.Product):
    return add_product(product)

@app.post("/api/stores")
async def add_store_api(store: schemas.Store):
    return add_store(store)

@app.delete("/api/products/{product_id}")
async def delete_product_api(product_id: int):
    return delete_product(product_id)

@app.delete("/api/stores/{store_id}")
async def delete_store_api(store_id: int):
    return delete_store(store_id)

@app.get("/api/logs")
async def get_logs_api():
    return get_logs()

@app.post("/api/stock/check")
async def check_stock(request: schemas.StockCheckRequest):
    try:
        result = services.check_stock(request.product_id, request.store_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stock/update")
async def update_stock(request: schemas.StockUpdateRequest):
    try:
        result = services.update_stock(
            request.product_id, request.store_id, request.quantity, request.operation
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stock/history")
async def get_stock_history(
    product_id: int = Query(None), store_id: int = Query(None)
):
    try:
        result = services.get_stock_history(product_id, store_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_server():
    """Uvicorn 서버를 실행하는 함수"""
    print("7. 서버를 시작합니다...")
    print("   주소: http://127.0.0.1:8000")
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except Exception as e:
        print(f"서버 시작 중 오류 발생: {e}")
        input("Enter를 눌러 종료하세요...")

if __name__ == "__main__":
    print("8. 메인 실행 시작...")
    
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("9. 서버 스레드가 시작되었습니다.")
    print("10. 브라우저를 열고 있습니다...")

    webbrowser.open("http://127.0.0.1:8000")

    try:
        print("11. 프로그램이 실행 중입니다. 종료하려면 Enter를 누르세요.")
        input()
    except Exception as e:
        print(f"오류 발생: {e}")
        input("Enter를 눌러 종료하세요...")
