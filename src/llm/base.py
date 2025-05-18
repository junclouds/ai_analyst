from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

class BaseLLM(ABC):
    """LLM基础类，定义统一接口"""
    
    def __init__(self, model_config: Dict[str, Any]):
        self.model_config = model_config
        self.model = self._initialize_model()
    
    @abstractmethod
    def _initialize_model(self) -> Any:
        """初始化模型"""
        pass
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """生成回复"""
        pass
    
    @abstractmethod
    async def generate_with_history(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """基于历史对话生成回复"""
        pass
    
    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """文本向量化"""
        pass 