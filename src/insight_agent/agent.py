from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime

from llm.base import BaseLLM
from utils.logger import get_logger
from utils.notification import NotificationManager

logger = get_logger(__name__)

class InsightAgent:
    """主动洞察Agent类"""
    
    def __init__(
        self,
        llm: BaseLLM,
        notification_manager: NotificationManager,
        config: Dict[str, Any]
    ):
        self.llm = llm
        self.notification_manager = notification_manager
        self.config = config
        self.running = False
        self._initialize_prompts()
    
    def _initialize_prompts(self):
        """初始化提示模板"""
        self.insight_prompt = """分析以下数据，找出重要的异常模式、趋势变化或需要关注的指标：

数据概览:
{data_summary}

历史趋势:
{historical_trends}

请提供：
1. 发现的关键洞察
2. 可能的原因分析
3. 建议的行动方案

如果发现严重异常，请特别标注。"""
    
    async def analyze_data(
        self,
        data_summary: str,
        historical_trends: str
    ) -> Dict[str, Any]:
        """分析数据并生成洞察"""
        prompt = self.insight_prompt.format(
            data_summary=data_summary,
            historical_trends=historical_trends
        )
        
        response = await self.llm.generate(prompt=prompt)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "insights": response,
            "data_summary": data_summary,
            "historical_trends": historical_trends
        }
    
    async def _scan_loop(self):
        """定期扫描数据的主循环"""
        while self.running:
            try:
                # 获取最新数据
                data_summary = "TODO: 实现数据获取逻辑"
                historical_trends = "TODO: 实现历史趋势获取逻辑"
                
                # 分析数据
                insights = await self.analyze_data(
                    data_summary=data_summary,
                    historical_trends=historical_trends
                )
                
                # 发送通知
                if self._should_notify(insights):
                    await self.notification_manager.send_notification(
                        title="新的数据洞察",
                        content=insights["insights"],
                        level="info"
                    )
                
                # 等待下一次扫描
                await asyncio.sleep(
                    self.config["scan_interval_minutes"] * 60
                )
                
            except Exception as e:
                logger.error(f"Error in scan loop: {str(e)}")
                await asyncio.sleep(60)  # 错误后等待1分钟再重试
    
    def _should_notify(self, insights: Dict[str, Any]) -> bool:
        """判断是否需要发送通知"""
        # TODO: 实现通知触发逻辑
        return True
    
    async def start(self):
        """启动Agent"""
        if not self.running:
            self.running = True
            asyncio.create_task(self._scan_loop())
            logger.info("Insight Agent started")
    
    async def stop(self):
        """停止Agent"""
        if self.running:
            self.running = False
            logger.info("Insight Agent stopped") 