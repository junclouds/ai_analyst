from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from utils.config import VectorStoreConfig

class BaseRetriever(ABC):
    """检索器基类"""
    
    @abstractmethod
    def __init__(self, config: VectorStoreConfig):
        """初始化检索器"""
        pass
    
    @abstractmethod
    async def add_documents(
        self,
        documents: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """添加文档到知识库"""
        pass
    
    @abstractmethod
    async def search(
        self,
        query: str,
        filter_criteria: Optional[Dict[str, Any]] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """搜索相关文档"""
        pass
    
    @abstractmethod
    async def delete_documents(
        self,
        document_ids: List[str]
    ) -> bool:
        """删除文档"""
        pass
    
    @abstractmethod
    async def update_document(
        self,
        document_id: str,
        document: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """更新文档"""
        pass 