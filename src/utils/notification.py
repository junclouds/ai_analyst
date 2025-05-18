import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiohttp
from typing import Dict, Any, Optional
from utils.config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class NotificationManager:
    """通知管理器"""
    
    def __init__(self):
        self.config = settings.insight_agent.alert_channels
    
    async def send_notification(
        self,
        title: str,
        content: str,
        level: str = "info"
    ) -> bool:
        """发送通知"""
        success = True
        
        for channel in self.config:
            try:
                if channel["type"] == "email":
                    await self._send_email(
                        title=title,
                        content=content,
                        config=channel["config"]
                    )
                elif channel["type"] == "slack":
                    await self._send_slack(
                        title=title,
                        content=content,
                        config=channel["config"]
                    )
            except Exception as e:
                logger.error(f"Failed to send notification via {channel['type']}: {str(e)}")
                success = False
        
        return success
    
    async def _send_email(
        self,
        title: str,
        content: str,
        config: Dict[str, Any]
    ) -> None:
        """发送邮件"""
        msg = MIMEMultipart()
        msg["Subject"] = title
        msg["From"] = config["sender"]
        msg["To"] = config["sender"]  # 发给自己
        
        msg.attach(MIMEText(content, "plain"))
        
        with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
            server.starttls()
            server.login(config["sender"], config["password"])
            server.send_message(msg)
    
    async def _send_slack(
        self,
        title: str,
        content: str,
        config: Dict[str, Any]
    ) -> None:
        """发送Slack消息"""
        message = f"*{title}*\n\n{content}"
        
        async with aiohttp.ClientSession() as session:
            await session.post(
                config["webhook_url"],
                json={"text": message}
            ) 