from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_client import make_asgi_app

from api.router import api_router
from utils.config import settings
from utils.logger import setup_logging
from handlers.error_handlers import setup_exception_handlers
from utils.rate_limiter import RateLimitMiddleware

# 设置日志
logger = setup_logging()

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.app.debug,
    ) 