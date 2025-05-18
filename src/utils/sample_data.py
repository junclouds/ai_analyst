from typing import List, Dict, Any
from retriever.chroma_retriever import ChromaRetriever
from utils.logger import get_logger

logger = get_logger(__name__)

# 示例文档数据
SAMPLE_DOCUMENTS = [
    {
        "content": """
销售业绩概览：2024年第二季度
总销售额：￥12,450,000，同比增长15.3%，环比增长8.7%
按区域划分：
- 华东区：￥4,850,000（39%），同比增长18.5%
- 华北区：￥3,250,000（26%），同比增长12.3%
- 华南区：￥2,750,000（22%），同比增长14.7%
- 西部区：￥1,600,000（13%），同比增长13.2%
最佳表现产品线：企业解决方案（￥5,320,000），占总销售额的42.7%
销售漏斗转化率：询盘到成交 28.5%（较上季度提升2.3个百分点）
平均销售周期：企业客户65天，中小企业客户38天
        """,
        "metadata": {
            "category": "sales",
            "date": "2024-06-30",
            "department": "sales",
            "type": "quarterly_report"
        }
    },
    {
        "content": """
营销效果分析：2024年第二季度
总体营销预算：￥1,850,000
各渠道ROI：
- 搜索引擎广告：287%（投资￥420,000）
- 社交媒体：215%（投资￥380,000）
- 电子邮件营销：189%（投资￥280,000）
- 内容营销：156%（投资￥350,000）
- 联盟营销：132%（投资￥230,000）
- 线下活动：121%（投资￥190,000）

获客成本（CAC）：
- 企业客户：￥12,800 / 客户
- 中小企业：￥4,300 / 客户
- 个人用户：￥820 / 客户

最佳表现广告系列：企业数字化转型方案（转化率8.7%，ROI 342%）
最佳获客渠道：专业技术博客引流（质量分数85/100）
        """,
        "metadata": {
            "category": "marketing",
            "date": "2024-06-30",
            "department": "marketing",
            "type": "quarterly_report"
        }
    },
    {
        "content": """
客户成功数据：2024年第二季度
总活跃客户：1,250家
客户续约率：92.3%（较上季度提升1.5个百分点）
NPS评分：78（优秀，位于行业前25%）

客户使用情况：
- 日活跃率：78.5%
- 周活跃率：92.3%
- 月活跃率：97.1%
- 平均每周使用时长：4.2小时/用户

功能使用率（前5名）：
1. 数据分析：92%
2. 自动报表：87%
3. 预测模型：76%
4. API集成：68%
5. 自定义仪表板：63%

流失风险客户：28家（其中高风险12家，中风险16家）
客户健康分布：优秀65%，良好25%，一般8%，需关注2%
        """,
        "metadata": {
            "category": "customer",
            "date": "2024-06-30",
            "department": "customer_success",
            "type": "quarterly_report"
        }
    },
    {
        "content": """
供应链报告：2024年第二季度
总采购金额：￥8,350,000
库存周转率：8.3次/季度

主要物料供应情况：
- 服务器设备：按需交付率97.5%
- 网络设备：按需交付率98.2%
- 办公设备：按需交付率99.5%

供应商绩效：
- A级供应商：7家（绩效得分≥90分）
- B级供应商：12家（绩效得分80-89分）
- C级供应商：5家（绩效得分70-79分）
- D级供应商：2家（绩效得分<70分，建议更换）

供应链瓶颈：
1. 高性能GPU交付周期延长（平均延迟15天）
2. 芯片供应短缺导致部分服务器配置降级
3. 国际物流成本上涨23.5%

库存情况：
- 正常库存：85%
- 高库存（>120天）：7%
- 低库存（<30天）：8%
        """,
        "metadata": {
            "category": "supply_chain",
            "date": "2024-06-30",
            "department": "operations",
            "type": "quarterly_report"
        }
    },
]

async def initialize_sample_data(retriever: ChromaRetriever) -> bool:
    """初始化示例数据到知识库"""
    try:
        logger.info("开始初始化示例数据")
        
        # 添加示例文档
        success = await retriever.add_documents(SAMPLE_DOCUMENTS)
        
        if success:
            logger.info(f"成功添加了 {len(SAMPLE_DOCUMENTS)} 条示例数据")
        else:
            logger.error("添加示例数据失败")
        
        return success
        
    except Exception as e:
        logger.error(f"初始化示例数据时出错: {str(e)}")
        return False 