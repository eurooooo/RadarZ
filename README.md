# RadarZ 🚀

> 智能 GitHub 项目发现工具 - 基于意图驱动的项目推荐系统

## 📖 项目简介

RadarZ 是一个智能 GitHub 项目发现工具，旨在解决"如何找到一个真正适合我当前需求的 GitHub 项目"这一核心问题。

与传统的关键词搜索不同，RadarZ 通过 AI 理解你的真实意图，智能生成搜索策略，并为你推荐真正匹配需求的项目。

### 核心特性

- 🎯 **意图驱动搜索** - 理解你的真实需求，而非简单的关键词匹配
- 🤖 **AI 智能推荐** - 使用 LangGraph + ReAct 框架进行深度分析和推荐
- ⚡ **流式返回** - 实时展示搜索结果，优化用户体验
- 📊 **项目摘要** - 自动生成项目深度分析，包括技术栈、适用场景等
- 🔍 **智能验证** - 自动验证项目质量、活跃度和维护状态
- 📈 **Trending 浏览** - 发现当日热门 GitHub 项目

## 🏗️ 技术架构

### 后端 (Backend)

- **框架**: FastAPI
- **AI 框架**: LangChain + LangGraph
- **推理模式**: ReAct (Reasoning + Acting)
- **主要依赖**:
  - `langchain` - AI 工作流编排
  - `langgraph` - 状态图管理
  - `langchain-google-genai` / `langchain-openai` - LLM 集成
  - `tavily-python` - 网络搜索
  - `fastapi` - API 服务

### 前端 (Frontend)

- **框架**: Next.js 16 (App Router)
- **UI 库**: React 19 + TypeScript
- **样式**: Tailwind CSS 4
- **图标**: Lucide React

## 🚀 快速开始

### 环境要求

- Python >= 3.12
- Node.js >= 18
- pnpm (推荐) 或 npm/yarn

### 后端设置

1. 进入后端目录：

```bash
cd backend
```

2. 安装依赖（使用 uv 或 pip）：

```bash
# 使用 uv (推荐)
uv sync

# 或使用 pip
pip install -e .
```

3. 配置环境变量：
   创建 `.env` 文件，添加必要的 API 密钥：

```env
GITHUB_TOKEN=your_github_token
GOOGLE_API_KEY=your_google_api_key  # 或使用 OPENAI_API_KEY
TAVILY_API_KEY=your_tavily_api_key
```

4. 启动后端服务：

```bash
uvicorn main:app --reload
```

后端服务将在 `http://localhost:8000` 启动。

### 前端设置

1. 进入前端目录：

```bash
cd frontend
```

2. 安装依赖：

```bash
pnpm install
# 或
npm install
```

3. 启动开发服务器：

```bash
pnpm dev
# 或
npm run dev
```

前端应用将在 `http://localhost:3000` 启动。

## 📡 API 端点

### 搜索项目

```
GET /search?user_input=你的搜索需求
```

流式返回匹配的 GitHub 项目。

### 获取项目摘要

```
GET /summary?repo_name=owner/repo&max_steps=10
```

使用 ReAct 框架生成项目深度分析。

### 获取 Trending 项目

```
GET /projects
```

返回当日 GitHub trending 项目列表。

## 🎯 使用示例

### 搜索示例

- "我想做一个个人知识库 RAG，偏 demo，但代码要清楚"
- "生产可用的 RAG 系统，支持权限、多租户"
- "学习 RAG 的工程结构，Python 实现"
- "Next.js 仪表盘模板，支持 TypeScript"

RadarZ 会理解你的意图，生成合适的搜索策略，并推荐匹配的项目。

## 🔧 项目结构

```
RadarZ/
├── backend/                 # 后端服务
│   ├── main.py             # FastAPI 应用入口
│   ├── src/
│   │   ├── agent/          # 传统 Agent 工作流
│   │   ├── React/          # ReAct 框架实现
│   │   ├── searchagent/    # 搜索 Agent
│   │   ├── github/         # GitHub API 客户端
│   │   └── models.py       # 数据模型
│   └── pyproject.toml      # Python 依赖配置
│
└── frontend/               # 前端应用
    ├── app/                # Next.js App Router
    │   ├── page.tsx        # 首页
    │   ├── explore/        # 项目浏览页
    │   └── project/        # 项目详情页
    ├── components/         # React 组件
    │   ├── SearchBar.tsx   # 搜索栏
    │   ├── SearchResults.tsx # 搜索结果
    │   └── ...
    └── hooks/              # React Hooks
        └── useSearch.ts    # 搜索逻辑
```

## 🧠 工作原理

### 搜索流程

1. **意图理解** - AI 分析用户输入，理解真实需求
2. **查询生成** - 生成多个精准的 GitHub 搜索查询
3. **项目搜索** - 并行执行多个搜索查询
4. **项目验证** - 使用 AI 验证每个项目是否符合需求
5. **流式返回** - 实时返回验证通过的项目

### 摘要生成流程

使用 ReAct (Reasoning + Acting) 框架：

1. **Think** - 分析项目 README，决定需要哪些额外信息
2. **Act** - 执行动作（搜索相关信息、分析代码结构等）
3. **Observe** - 观察结果，决定是否继续深入
4. **总结** - 生成全面的项目分析报告

## 🛣️ 路线图

查看 [Roadmap.md](./backend/Roadmap.md) 了解详细的功能规划。

主要方向：

- 个性化推荐系统
- 更智能的项目质量评估
- 多模态项目分析（代码、文档、社区讨论）
- 成本优化和性能提升

## 📝 许可证

本项目采用 MIT 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请通过 GitHub Issues 联系我们。

---

**RadarZ** - 让 GitHub 项目发现变得智能而简单 ✨

```

这是一个 README 草稿，包含：
- 项目简介与核心特性
- 技术架构说明
- 快速开始指南
- API 文档
- 使用示例
- 项目结构
- 工作原理说明
- 路线图链接

需要调整或补充的部分请告知。
```
