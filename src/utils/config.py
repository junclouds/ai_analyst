import os
from pathlib import Path
from typing import Any, Dict
import yaml
from pydantic import BaseModel
from dotenv import load_dotenv

# 尝试加载环境变量，但不强制要求
try:
    load_dotenv()
except Exception:
    pass

# 默认配置
DEFAULT_CONFIG = {
    "app": {
        "name": "AI Analyst",
        "version": "1.0.0",
        "debug": True,
        "log_level": "INFO"
    },
    "api": {
        "host": "0.0.0.0",
        "port": 8000,
        "prefix": "/api/v1",
        "cors_origins": ["*"],
        "rate_limit": {
            "requests_per_minute": 60,
            "burst_limit": 100
        }
    },
    "security": {
        "jwt_secret": os.getenv("JWT_SECRET", "dev-secret-key"),
        "token_expire_minutes": 1440,
        "algorithm": "HS256"
    },
    "cache": {
        "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        "default_ttl": 3600
    },
    "llm": {
        "default_provider": "ollama",
        "providers": {
            "ollama": {
                "model": "qwen3:0.6b",
                "temperature": 0.7,
                "max_tokens": 2000,
                "api_base": "http://localhost:11434"
            },
            "openai": {
                "model": "gpt-4-turbo-preview",
                "temperature": 0.7,
                "max_tokens": 2000,
                "api_key": os.getenv("OPENAI_API_KEY", "")
            }
        }
    },
    "vector_store": {
        "provider": "chroma",
        "collection_name": "ai_analyst",
        "embedding_model": "all-MiniLM-L6-v2"
    },
    "data_sources": {},
    "insight_agent": {
        "scan_interval_minutes": 60,
        "alert_channels": []
    }
}

def _load_yaml_config() -> Dict[str, Any]:
    """加载YAML配置文件"""
    try:
        config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return DEFAULT_CONFIG
    except Exception:
        return DEFAULT_CONFIG

def _replace_env_vars(config: Dict[str, Any]) -> Dict[str, Any]:
    """替换配置中的环境变量"""
    if isinstance(config, dict):
        return {k: _replace_env_vars(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [_replace_env_vars(v) for v in config]
    elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
        env_var = config[2:-1]
        return os.getenv(env_var, "")
    return config

class AppConfig(BaseModel):
    name: str
    version: str
    debug: bool
    log_level: str

class RateLimitConfig(BaseModel):
    requests_per_minute: int
    burst_limit: int

class ApiConfig(BaseModel):
    host: str
    port: int
    prefix: str
    cors_origins: list[str]
    rate_limit: RateLimitConfig

class SecurityConfig(BaseModel):
    jwt_secret: str
    token_expire_minutes: int
    algorithm: str

class CacheConfig(BaseModel):
    redis_url: str
    default_ttl: int

class LLMProviderConfig(BaseModel):
    model: str
    temperature: float
    max_tokens: int
    api_key: str = ""
    api_base: str = ""

class LLMConfig(BaseModel):
    default_provider: str
    providers: Dict[str, LLMProviderConfig]

class VectorStoreConfig(BaseModel):
    provider: str
    collection_name: str
    embedding_model: str = "nomic-embed-text"  # 默认使用 nomic-embed-text
    ollama_api_base: str = "http://localhost:11434"
    openai_api_key: str = ""

class Settings(BaseModel):
    app: AppConfig
    api: ApiConfig
    security: SecurityConfig
    cache: CacheConfig
    llm: LLMConfig
    vector_store: VectorStoreConfig
    data_sources: Dict[str, Dict[str, str]]
    insight_agent: Dict[str, Any]

# 加载配置
_config = _load_yaml_config()
_config = _replace_env_vars(_config)
settings = Settings(**_config) 