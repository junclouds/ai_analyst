from typing import Optional
import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from utils.cache import Cache

class RateLimitMiddleware(BaseHTTPMiddleware):
    """请求限流中间件"""
    
    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        burst_limit: int = 100
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit
        self.cache = Cache()
    
    async def dispatch(
        self,
        request: Request,
        call_next
    ):
        # 获取客户端IP
        client_ip = request.client.host
        
        # 检查是否超过突发限制
        burst_key = f"rate_limit:burst:{client_ip}"
        burst_count = await self.cache.get(burst_key) or 0
        
        if burst_count >= self.burst_limit:
            raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )
        
        # 检查是否超过每分钟请求限制
        minute_key = f"rate_limit:minute:{client_ip}"
        minute_count = await self.cache.get(minute_key) or 0
        
        if minute_count >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )
        
        # 更新计数器
        await self.cache.set(burst_key, burst_count + 1, ttl=1)  # 1秒
        await self.cache.set(minute_key, minute_count + 1, ttl=60)  # 1分钟
        
        # 处理请求
        response = await call_next(request)
        return response 