from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from qa_engine.engine import QAEngine
from insight_agent.agent import InsightAgent
from llm.ollama_llm import OllamaLLM
from retriever.chroma_retriever import ChromaRetriever
from utils.cache import Cache
from utils.notification import NotificationManager
from utils.config import settings

# 创建路由
api_router = APIRouter()

# 创建依赖
def get_qa_engine() -> QAEngine:
    """获取问答引擎实例"""
    llm = OllamaLLM(settings.llm.providers[settings.llm.default_provider].dict())
    retriever = ChromaRetriever(settings.vector_store)
    cache = Cache()
    return QAEngine(llm, retriever, cache, settings.dict())

def get_insight_agent() -> InsightAgent:
    """获取洞察Agent实例"""
    llm = OllamaLLM(settings.llm.providers[settings.llm.default_provider].dict())
    notification_manager = NotificationManager()
    return InsightAgent(llm, notification_manager, settings.insight_agent)

# 定义请求/响应模型
class QuestionRequest(BaseModel):
    question: str
    chat_history: Optional[List[Dict[str, str]]] = None

class QuestionResponse(BaseModel):
    answer: str
    context: Optional[str] = None
    visualization: Optional[Dict[str, Any]] = None

class DocumentRequest(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None

class InsightResponse(BaseModel):
    timestamp: str
    insights: str
    data_summary: str
    historical_trends: str

# 定义路由
@api_router.post("/qa", response_model=QuestionResponse)
async def answer_question(request: QuestionRequest):
    """回答问题接口"""
    try:
        # 初始化组件
        llm = OllamaLLM(settings.llm.providers[settings.llm.default_provider].dict())
        retriever = ChromaRetriever(settings.vector_store)
        cache = Cache()
        
        # 创建问答引擎
        engine = QAEngine(
            llm=llm,
            retriever=retriever,
            cache=cache,
            config=settings.dict()
        )
        
        # 获取答案
        result = await engine.answer_question(
            question=request.question,
            chat_history=request.chat_history
        )
        
        return QuestionResponse(
            answer=result["answer"],
            context=result.get("context"),
            visualization=result.get("visualization")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"问答服务错误: {str(e)}"
        )

@api_router.post("/documents")
async def add_document(
    request: DocumentRequest,
    qa_engine: QAEngine = Depends(get_qa_engine)
) -> Dict[str, bool]:
    """添加文档接口"""
    try:
        success = await qa_engine.retriever.add_documents(
            documents=[{
                "content": request.content,
                "metadata": request.metadata
            }]
        )
        return {"success": success}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add document: {str(e)}"
        )

@api_router.get("/insights", response_model=InsightResponse)
async def get_latest_insights(
    agent: InsightAgent = Depends(get_insight_agent)
) -> Dict[str, Any]:
    """获取最新洞察接口"""
    try:
        return await agent.analyze_data(
            data_summary="示例数据概览",
            historical_trends="示例历史趋势"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get insights: {str(e)}"
        ) 