from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_client import make_asgi_app
import asyncio

from api.router import api_router
from utils.config import settings
from utils.logger import setup_logging, get_logger
from handlers.error_handlers import setup_exception_handlers
from utils.rate_limiter import RateLimitMiddleware
# 暂时注释掉示例数据初始化相关导入
# from utils.sample_data import initialize_sample_data
# from retriever.chroma_retriever import ChromaRetriever

# 设置日志
setup_logging()  # 只调用设置函数，不赋值
logger = get_logger(__name__)  # 使用get_logger获取logger

app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    description="Enterprise AI Analyst API",
)

# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=settings.api.rate_limit.requests_per_minute,
    burst_limit=settings.api.rate_limit.burst_limit,
)

# 设置异常处理器
setup_exception_handlers(app)

# 添加路由
app.include_router(api_router, prefix=settings.api.prefix)

# 添加静态文件支持
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")

# 添加 Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 简化启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行的操作"""
    logger.info("应用启动")

if __name__ == "__main__":
    import uvicorn
    import os
    
    # 添加当前目录到 Python 路径
    import sys
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
    
    uvicorn.run(
        "src.main:app",
        host=settings.api.host,
        port=8080,  # 使用8080端口
        reload=settings.app.debug,
    ) 