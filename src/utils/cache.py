from typing import Any, Optional
import json
from datetime import datetime, timedelta
from utils.logger import get_logger

logger = get_logger(__name__)

class Cache:
    """缓存实现类，使用内存作为后端存储"""
    
    def __init__(self):
        """初始化内存存储"""
        self._storage = {}
        self._expiry = {}
        self.default_ttl = 3600  # 默认1小时过期
    
    async def connect(self):
        """内存存储不需要连接"""
        pass
    
    def _is_expired(self, key: str) -> bool:
        """检查键是否过期"""
        if key in self._expiry:
            return datetime.now() > self._expiry[key]
        return False
    
    def _clean_expired(self):
        """清理过期的键"""
        now = datetime.now()
        expired_keys = [k for k, v in self._expiry.items() if now > v]
        for key in expired_keys:
            self._storage.pop(key, None)
            self._expiry.pop(key, None)
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        try:
            self._clean_expired()
            if key in self._storage and not self._is_expired(key):
                return self._storage[key]
            return None
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """设置缓存值"""
        try:
            self._storage[key] = value
            expiry_time = datetime.now() + timedelta(seconds=ttl or self.default_ttl)
            self._expiry[key] = expiry_time
            return True
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """删除缓存值"""
        try:
            self._storage.pop(key, None)
            self._expiry.pop(key, None)
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}")
            return False
    
    async def clear(self) -> bool:
        """清空所有缓存"""
        try:
            self._storage.clear()
            self._expiry.clear()
            return True
        except Exception as e:
            logger.error(f"Cache clear error: {str(e)}")
            return False 