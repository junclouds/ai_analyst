from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
from utils.logger import get_logger
from utils.notification import NotificationManager
from llm.base import BaseLLM

logger = get_logger(__name__)

class InsightAgent:
    """洞察Agent实现类，负责数据监控与主动分析"""
    
    def __init__(
        self,
        llm: BaseLLM,
        notification_manager: NotificationManager,
        config: Dict[str, Any]
    ):
        """初始化Agent"""
        self.llm = llm
        self.notification_manager = notification_manager
        self.config = config
        self.scan_interval = config.get("scan_interval_minutes", 60)
    
    async def start_monitoring(self):
        """启动监控任务"""
        logger.info("启动数据监控任务")
        while True:
            try:
                # 执行数据监控与分析
                insights = await self.analyze_data()
                
                # 如果有重要洞察，发送通知
                if insights and self._should_notify(insights):
                    await self.send_notifications(insights)
                
                # 等待到下一个扫描周期
                await asyncio.sleep(self.scan_interval * 60)
                
            except Exception as e:
                logger.error(f"数据监控任务出错: {str(e)}")
                await asyncio.sleep(60)  # 出错后等待1分钟再重试
    
    def _should_notify(self, insights: Dict[str, Any]) -> bool:
        """判断是否应该发送通知"""
        # 简单实现：如果有洞察内容就通知
        return len(insights.get("insights", "").strip()) > 0
    
    async def send_notifications(self, insights: Dict[str, Any]):
        """发送通知"""
        try:
            message = f"新的数据洞察 ({insights['timestamp']}):\n\n{insights['insights']}"
            
            # 发送通知
            channels = self.config.get("alert_channels", [])
            for channel in channels:
                await self.notification_manager.send(
                    channel=channel.get("type", "email"),
                    recipients=channel.get("recipients", []),
                    subject="AI分析师 - 数据洞察提醒",
                    message=message
                )
                
            logger.info(f"已发送洞察通知到 {len(channels)} 个渠道")
            
        except Exception as e:
            logger.error(f"发送通知时出错: {str(e)}")
    
    async def analyze_data(
        self,
        data_summary: str = "",
        historical_trends: str = ""
    ) -> Dict[str, Any]:
        """分析数据并生成洞察"""
        try:
            timestamp = datetime.now().isoformat()
            
            # 如果没有提供数据，这里应该是从数据源获取
            if not data_summary:
                data_summary = "当前无可用数据"
            
            if not historical_trends:
                historical_trends = "无历史趋势数据"
            
            # 构建提示
            prompt = f"""作为AI分析师，请基于以下信息提供业务洞察：
            
数据概况:
{data_summary}

历史趋势:
{historical_trends}

请分析上述数据，提供关键洞察、潜在机会和需要关注的风险。"""

            # 生成洞察
            insights = await self.llm.generate(prompt)
            
            return {
                "timestamp": timestamp,
                "insights": insights,
                "data_summary": data_summary,
                "historical_trends": historical_trends
            }
            
        except Exception as e:
            logger.error(f"生成数据洞察时出错: {str(e)}")
            return {
                "timestamp": datetime.now().isoformat(),
                "insights": f"无法生成洞察: {str(e)}",
                "data_summary": data_summary,
                "historical_trends": historical_trends
            } 