from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from utils.logger import get_logger

logger = get_logger(__name__)

def setup_exception_handlers(app: FastAPI) -> None:
    """设置异常处理器"""
    
    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        """全局异常处理器"""
        logger.error(f"Unhandled exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "message": str(exc)
            }
        ) 