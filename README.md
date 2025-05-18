# AI Analyst - 企业级个人化 AI 分析师系统

## 项目概述
AI Analyst 是一个基于大语言模型的智能数据分析系统，支持自然语言问答、主动数据洞察和多源数据接入。系统具备以下核心特性：

- 🤖 支持多种大语言模型（OpenAI、Claude、Gemini）
- 📊 接入多种数据源（Snowflake、BigQuery、Databricks）
- 💡 主动数据洞察与异常预警
- 🔍 基于文档和结构化数据的智能问答
- 🚀 高性能与可扩展性设计
- 🔒 企业级安全与权限控制

## 项目结构
```
ai_analyst/
├── config/                 # 配置文件目录
│   └── config.yaml        # 主配置文件
├── src/                   # 源代码目录
│   ├── api/              # API 路由与接口定义
│   ├── llm/              # 语言模型封装
│   ├── retriever/        # 数据检索模块
│   ├── qa_engine/        # 问答引擎核心
│   ├── insight_agent/    # 主动洞察 Agent
│   ├── utils/            # 工具函数
│   ├── handlers/         # 异常处理
│   └── main.py          # 应用入口
├── data/                 # 数据存储目录
├── examples/             # 示例代码
├── notebooks/            # Jupyter 笔记本
├── tests/               # 测试用例
├── Dockerfile           # 容器化配置
├── requirements.txt     # 依赖包列表
└── README.md           # 项目文档
```

## 快速开始

### 环境要求
- Python 3.11+
- Redis
- Vector Store (ChromaDB)

### 安装
1. 克隆仓库
```bash
git clone https://github.com/your-org/ai-analyst.git
cd ai-analyst
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息
```

### 运行
1. 启动服务
```bash
uvicorn src.main:app --reload
```

2. 访问 API 文档
```
http://localhost:8000/docs
```

## 开发指南

### 添加新的语言模型
1. 在 `src/llm/` 目录下创建新的模型实现类
2. 继承 `BaseLLM` 类并实现所有抽象方法
3. 在配置文件中添加新模型的配置项

### 添加新的数据源
1. 在 `src/retriever/` 目录下创建新的检索器实现
2. 继承 `BaseRetriever` 类并实现所有抽象方法
3. 在配置文件中添加新数据源的连接信息

### 自定义主动洞察规则
1. 修改 `src/insight_agent/agent.py` 中的分析逻辑
2. 在配置文件中更新洞察规则和通知阈值

## API 文档
详细的 API 文档请访问运行时的 Swagger UI：`http://localhost:8000/docs`

## 测试
运行单元测试：
```bash
pytest tests/
```

## 部署
1. 构建 Docker 镜像
```bash
docker build -t ai-analyst .
```

2. 运行容器
```bash
docker run -d -p 8000:8000 ai-analyst
```

## 贡献指南
1. Fork 项目
2. 创建特性分支
3. 提交变更
4. 推送到分支
5. 创建 Pull Request

## 许可证
MIT License 