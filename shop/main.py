# -*- coding: utf-8 -*-
"""
主程式檔
"""

from fastapi import FastAPI, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from utils.app import router
from utils.config import config, WebLogger


API = config['API']['url']
## swagger設定
app = FastAPI(
    title=config['Swagger']['title'],
    description=config['Swagger']['description'],
    version=config['Swagger']['version'],
    contact=config['Swagger']['contact'],
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    docs_url=f"/{API}/docs", #指定路徑
    openapi_url=f"/{API}/api/v1/openapi.json",
    openapi_tags=config['Swagger']['openapi_tags']
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["DNT","X-Mx-ReqToken","Keep-Alive","User-Agent","X-Requested-With","If-Modified-Since","Cache-Control","Content-Type","Authorization"],
)

app.include_router(router)

## 422錯誤回覆
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"Result": exc.errors(), "body": exc.body},
    )

## LOG 紀錄
@app.middleware("http")
async def log_request(request, call_next):
    try:
        response = await call_next(request)
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        
        log_params = {
            "method":request.method,
            "status_code":response.status_code,
            # "reply_body":body.decode('utf-8'), 加這個檔案傳輸會有問題
            "url_path":request.url,
            "header":dict(response.headers),
            "query_params":request.query_params,
            "client_host": request.client.host,
            "media_type":response.media_type
        }

        WebLogger.info(log_params)

        return Response(
            content=body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )
    
    except Exception as exc:
        WebLogger.error(exc)
        return JSONResponse(status_code=500, content={'reason': str(exc)})
    