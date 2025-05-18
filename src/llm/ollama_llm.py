from typing import Dict, Any, List, Optional
import json
import aiohttp
from .base import BaseLLM
from utils.logger import get_logger

logger = get_logger(__name__)

class OllamaLLM(BaseLLM):
    """Ollama LLM实现"""
    
    def _initialize_model(self) -> None:
        """初始化模型（Ollama不需要初始化）"""
        return None
    
    async def _make_request(
        self,
        endpoint: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """发送请求到Ollama API"""
        api_base = self.model_config.get("api_base", "http://localhost:11434")
        url = f"{api_base}/{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Ollama API error: {error_text}")
                return await response.json()
    
    async def generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """生成回复"""
        try:
            # 构建请求
            payload = {
                "model": self.model_config["model"],
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature or self.model_config.get("temperature", 0.7),
                    "num_predict": max_tokens or self.model_config.get("max_tokens", 2000),
                }
            }
            
            if system_message:
                payload["system"] = system_message
            
            # 发送请求
            response = await self._make_request("api/generate", payload)
            return response.get("response", "")
            
        except Exception as e:
            logger.error(f"Ollama generate error: {str(e)}")
            raise
    
    async def generate_with_history(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """基于历史对话生成回复"""
        try:
            # 构建对话历史
            formatted_messages = []
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "system":
                    formatted_messages.append({"system": content})
                else:
                    formatted_messages.append({"role": role, "content": content})
            
            # 构建请求
            payload = {
                "model": self.model_config["model"],
                "messages": formatted_messages,
                "stream": False,
                "options": {
                    "temperature": temperature or self.model_config.get("temperature", 0.7),
                    "num_predict": max_tokens or self.model_config.get("max_tokens", 2000),
                }
            }
            
            # 发送请求
            response = await self._make_request("api/chat", payload)
            return response.get("message", {}).get("content", "")
            
        except Exception as e:
            logger.error(f"Ollama generate_with_history error: {str(e)}")
            raise
    
    async def embed_text(self, text: str) -> List[float]:
        """文本向量化"""
        try:
            # 构建请求
            payload = {
                "model": self.model_config["model"],
                "prompt": text
            }
            
            # 发送请求
            response = await self._make_request("api/embeddings", payload)
            return response.get("embedding", [])
        except Exception as e:
            logger.error(f"Ollama embed_text error: {str(e)}")
            raise 