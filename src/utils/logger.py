import logging
import sys
from typing import Optional
from utils.config import settings

def setup_logging() -> None:
    """设置全局日志配置"""
    logging.basicConfig(
        level=getattr(logging, settings.app.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log')
        ]
    )

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """获取logger实例"""
    return logging.getLogger(name) 