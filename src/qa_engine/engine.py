from typing import Dict, Any, List, Optional
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from llm.base import BaseLLM
from retriever.base import BaseRetriever
from utils.logger import get_logger
from utils.cache import Cache

logger = get_logger(__name__)

class QAEngine:
    """问答引擎核心类"""
    
    def __init__(
        self,
        llm: BaseLLM,
        retriever: BaseRetriever,
        cache: Cache,
        config: Dict[str, Any]
    ):
        self.llm = llm
        self.retriever = retriever
        self.cache = cache
        self.config = config
        self._initialize_prompts()
    
    def _initialize_prompts(self):
        """初始化提示模板"""
        self.qa_prompt = PromptTemplate(
            template="""基于以下上下文信息回答问题。如果无法从上下文中找到答案，请明确说明。

上下文信息:
{context}

问题: {question}

请提供详细的回答，并引用相关的上下文信息源。""",
            input_variables=["context", "question"]
        )
    
    async def _get_relevant_context(
        self,
        question: str,
        filter_criteria: Optional[Dict[str, Any]] = None
    ) -> str:
        """获取相关上下文"""
        documents = await self.retriever.search(
            query=question,
            filter_criteria=filter_criteria
        )
        return "\n\n".join([doc["content"] for doc in documents])
    
    async def answer_question(
        self,
        question: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        filter_criteria: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """回答问题"""
        # 检查缓存
        cache_key = f"qa:{question}"
        if cached_response := await self.cache.get(cache_key):
            logger.info(f"Cache hit for question: {question}")
            return cached_response
        
        # 获取相关上下文
        context = await self._get_relevant_context(
            question=question,
            filter_criteria=filter_criteria
        )
        
        # 生成回答
        if chat_history:
            response = await self.llm.generate_with_history(
                messages=[
                    *chat_history,
                    {
                        "role": "system",
                        "content": self.qa_prompt.format(
                            context=context,
                            question=question
                        )
                    }
                ]
            )
        else:
            response = await self.llm.generate(
                prompt=self.qa_prompt.format(
                    context=context,
                    question=question
                )
            )
        
        result = {
            "question": question,
            "answer": response,
            "context": context
        }
        
        # 缓存结果
        await self.cache.set(cache_key, result)
        
        return result 