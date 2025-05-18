# AI 分析师

一个企业级的个性化 AI 分析助手系统，基于大语言模型和向量数据库构建。

## 功能特点

- 🤖 智能问答：基于文档上下文的准确回答
- 📊 数据分析：支持多种数据源的智能分析
- 🔍 知识库管理：文档的添加、检索和更新
- 🚀 高性能：异步处理和缓存优化
- 🛡️ 安全可靠：完整的错误处理和日志记录

## 技术栈

- Python 3.11+
- FastAPI
- LangChain
- ChromaDB
- Ollama / OpenAI
- Redis (可选)

## 快速开始

### 环境要求

- Python 3.11 或更高版本
- Ollama (用于本地 LLM 部署)
- Redis (可选，用于缓存)

### 安装

1. 克隆仓库：
```bash
git clone https://github.com/junclouds/ai_analyst.git
cd ai_analyst
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，设置必要的环境变量
```

### 运行

1. 启动服务：
```bash
python src/main.py
```

2. 访问 API 文档：
```
http://localhost:8000/docs
```

## API 接口

### 问答接口

- POST `/api/v1/qa`
  - 输入：问题文本和可选的聊天历史
  - 输出：AI 回答和相关上下文

### 文档管理

- POST `/api/v1/documents`
  - 添加新文档到知识库
  - 支持元数据标注

### 数据分析

- GET `/api/v1/insights`
  - 获取数据分析洞察
  - 支持自定义分析维度

## 配置说明

主要配置文件位于 `config/config.yaml`，包括：

- API 设置
- LLM 配置
- 向量存储设置
- 缓存配置
- 安全设置

## 开发指南

### 项目结构

```
ai_analyst/
├── config/             # 配置文件
├── src/
│   ├── api/           # API 路由
│   ├── llm/           # LLM 模型封装
│   ├── qa_engine/     # 问答引擎
│   ├── retriever/     # 检索模块
│   ├── utils/         # 工具函数
│   └── main.py        # 入口文件
├── tests/             # 测试用例
└── data/              # 数据目录
```

### 开发规范

- 使用 Python 类型注解
- 遵循 PEP 8 编码规范
- 编写单元测试
- 使用异步编程

## 部署

### Docker 部署

1. 构建镜像：
```bash
docker build -t ai-analyst .
```

2. 运行容器：
```bash
docker run -d -p 8000:8000 ai-analyst
```

### 生产环境配置

- 使用 Gunicorn 作为 WSGI 服务器
- 配置 NGINX 反向代理
- 启用 Redis 缓存
- 设置监控和告警

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License 