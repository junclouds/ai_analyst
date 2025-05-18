import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiohttp
from typing import Dict, Any, List, Optional
from utils.config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class NotificationManager:
    """通知管理器，负责发送各种类型的通知"""
    
    async def send(
        self,
        channel: str,
        recipients: List[str],
        subject: str,
        message: str,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> bool:
        """发送通知
        
        Args:
            channel: 通知渠道 (email, slack, teams等)
            recipients: 接收者列表
            subject: 主题
            message: 消息内容
            attachments: 附件列表
            
        Returns:
            发送成功返回True，否则返回False
        """
        try:
            # 根据不同渠道调用不同的发送方法
            if channel == "email":
                return await self._send_email(recipients, subject, message, attachments)
            elif channel == "slack":
                return await self._send_slack(recipients, subject, message, attachments)
            elif channel == "teams":
                return await self._send_teams(recipients, subject, message, attachments)
            else:
                logger.warning(f"不支持的通知渠道: {channel}")
                return False
                
        except Exception as e:
            logger.error(f"发送通知时出错: {str(e)}")
            return False
    
    async def _send_email(
        self,
        recipients: List[str],
        subject: str,
        message: str,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> bool:
        """发送邮件通知"""
        try:
            logger.info(f"发送邮件到 {recipients}，主题：{subject}")
            
            # 如果配置了SMTP，使用实际发送
            if hasattr(settings, 'email_config'):
                config = settings.email_config
                msg = MIMEMultipart()
                msg["Subject"] = subject
                msg["From"] = config.sender
                msg["To"] = ", ".join(recipients)
                
                msg.attach(MIMEText(message, "plain"))
                
                with smtplib.SMTP(config.smtp_server, config.smtp_port) as server:
                    server.starttls()
                    server.login(config.sender, config.password)
                    server.send_message(msg)
            else:
                # 否则只记录日志
                logger.info(f"模拟发送邮件: {message[:100]}...")
                
            return True
        except Exception as e:
            logger.error(f"邮件发送失败: {str(e)}")
            return False
    
    async def _send_slack(
        self,
        recipients: List[str],
        subject: str,
        message: str,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> bool:
        """发送Slack通知"""
        try:
            logger.info(f"发送Slack消息，主题：{subject}")
            
            # 如果配置了Slack Webhook
            if hasattr(settings, 'slack_config') and settings.slack_config.webhook_url:
                webhook_url = settings.slack_config.webhook_url
                formatted_message = f"*{subject}*\n\n{message}"
                
                async with aiohttp.ClientSession() as session:
                    await session.post(
                        webhook_url,
                        json={"text": formatted_message}
                    )
            else:
                # 否则只记录日志
                logger.info(f"模拟发送Slack消息: {message[:100]}...")
                
            return True
        except Exception as e:
            logger.error(f"Slack消息发送失败: {str(e)}")
            return False
    
    async def _send_teams(
        self,
        recipients: List[str],
        subject: str,
        message: str,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> bool:
        """发送Teams通知（示例实现）"""
        # 简单记录日志
        logger.info(f"模拟发送Teams消息到 {recipients}")
        return True 