from typing import Dict, Any, List, Optional
import chromadb
from chromadb.config import Settings
import aiohttp
import numpy as np
from .base import BaseRetriever
from utils.logger import get_logger
from utils.config import VectorStoreConfig

logger = get_logger(__name__)

class ChromaRetriever(BaseRetriever):
    """ChromaDB检索器实现"""
    
    def __init__(self, config: VectorStoreConfig):
        """初始化检索器"""
        self.config = config
        self.client = self._initialize_client()
    
    def _initialize_client(self) -> chromadb.Client:
        """初始化ChromaDB客户端"""
        client = chromadb.Client(
            Settings(
                persist_directory="data/chroma",
                is_persistent=True,
                anonymized_telemetry=False  # 关闭遥测
            )
        )
        
        # 获取或创建集合
        self.collection = client.get_or_create_collection(
            name=self.config.collection_name
        )
        
        return client
    
    async def add_documents(
        self,
        documents: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """添加文档到知识库"""
        try:
            # 准备数据
            ids = [str(i) for i in range(len(documents))]
            texts = [doc["content"] for doc in documents]
            metadatas = [
                {**doc.get("metadata", {}), **(metadata or {})}
                for doc in documents
            ]
            
            # 添加到集合
            self.collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )
            
            return True
            
        except Exception as e:
            logger.error(f"ChromaDB add_documents error: {str(e)}")
            return False
    
    async def search(
        self,
        query: str,
        filter_criteria: Optional[Dict[str, Any]] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """搜索相关文档"""
        try:
            # 执行搜索
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=filter_criteria
            )
            
            # 格式化结果
            documents = []
            for i in range(len(results["documents"][0])):
                documents.append({
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i]
                })
            
            return documents
            
        except Exception as e:
            logger.error(f"ChromaDB search error: {str(e)}")
            return []
    
    async def delete_documents(
        self,
        document_ids: List[str]
    ) -> bool:
        """删除文档"""
        try:
            self.collection.delete(ids=document_ids)
            return True
        except Exception as e:
            logger.error(f"ChromaDB delete_documents error: {str(e)}")
            return False
    
    async def update_document(
        self,
        document_id: str,
        document: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """更新文档"""
        try:
            self.collection.update(
                ids=[document_id],
                documents=[document["content"]],
                metadatas=[{
                    **document.get("metadata", {}),
                    **(metadata or {})
                }]
            )
            return True
        except Exception as e:
            logger.error(f"ChromaDB update_document error: {str(e)}")
            return False 