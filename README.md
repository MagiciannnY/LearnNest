# 🪺 LearnNest

> 一个支持语义检索与大模型问答的（数据库）学习助手系统

## 📘 项目简介

**LearnNest** 是一个基于本地知识向量检索与大语言模型交互的学习助手系统。用户可以上传 PDF、Word、PPT、Markdown、文本等格式的学习资料，系统会自动将文档切块、生成语义向量，并存入本地 PostgreSQL 数据库（使用 pgvector）。当用户提出问题时，系统通过向量相似度检索相关知识片段，构造上下文，最终调用 DeepSeek Chat 接口生成带上下文的智能回答。

前端采用 ChatGPT 风格的对话界面，支持流式输出、Markdown 渲染与对话记录展示，提供沉浸式、上下文感知的学习体验。

## 🚀 项目内容

* 📄 支持多种文件格式上传（.pdf, .docx, .pptx, .md, .txt, .doc, .ppt）
* 🧠 使用 `doubao-embedding-large-text-240915` 嵌入模型构建4096维向量索引
* 🗂 本地向量数据库（PostgreSQL + pgvector）语义检索
* 🤖 接入 DeepSeek Chat API 实现上下文增强问答（RAG）
* 💬 前端仿 ChatGPT 聊天气泡界面，支持 Markdown
* 🔁 流式响应

---

## 🧱 技术架构

| 层级   | 技术/组件                                  |
| ---- | -------------------------------------- |
| 前端   | Vue3 + Tailwind CSS                    |
| 后端   | FastAPI + httpx                        |
| 嵌入模型 | doubao-embedding-large-text-240915     |
| 大模型  | DeepSeek Chat API                      |
| 数据库  | PostgreSQL + pgvector                  |
| 文件解析 | pdfminer.six, python-docx, python-pptx |

---

## ⚙️ 部署与启动

### 1️⃣ 安装依赖环境

> 推荐使用 Python 3.10+ 和 Node.js 18+

#### ✅ Python 环境依赖

```bash
python -m venv venv
source venv/bin/activate  # 或 Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### ✅ Node.js + 前端依赖

```bash
cd frontend
npm install
```

### 2️⃣ 配置环境变量（`.env`）

在项目根目录创建 `.env` 文件：

```env
DATABASE_URL=你需要连接的数据库
EMBEDDING_API_KEY=你的豆包API密钥
EMBEDDING_MODEL=doubao-embedding-large-text-240915
EMBEDDING_API_BASE=https://ark.cn-beijing.volces.com/api/v3
LLM_API_KEY=你的DeepSeek API密钥
LLM_MODEL=deepseek-chat
LLM_API_BASE=https://api.deepseek.com
```

`config.py` 会从 `.env` 中读取信息

### 3️⃣ 初始化数据库结构

在首次部署时，需运行初始化脚本创建表结构：

```bash
python app/init_db.py
```

该脚本将自动创建存储向量与知识块的 `knowledge_chunks` 表结构。

### 4️⃣ 启动后端服务

```bash
uvicorn app.main:app --host localhost --port 8002 --reload
```

### 5️⃣ 启动前端服务

```bash
cd frontend
npm run dev
```

浏览器访问：[http://localhost:5173](http://localhost:5173)

---

## ✅ 使用说明

1. 在左侧上传学习资料（支持多个文件）
2. 右侧提问输入栏中输入问题
3. 系统将实时展示语义检索+大模型回答结果
4. 支持上下文连续提问

---

## 📌 TODO（开发中功能）

* 支持知识点标签与章节结构标注：为每个知识块自动/手动添加标签与所属章节，提升语义组织性与检索维度。
* 增加用户身份体系：引入用户登录鉴权，支持私有知识库管理、历史记录与个性化内容生成。
* 文件级与内容级检索功能：支持按文件名、段落内容、关键词等多维方式检索已有知识块。
* 可视化查看上传文件与知识块：上传后可浏览文件结构与切块信息，支持点击查看、跳转与管理。
* 引入知识图谱增强问答：结合实体识别与关系推理构建知识图谱，提升多跳问答与复杂问题理解能力。
* 支持多学科内容管理：构建多个独立知识库，按学科/领域划分向量空间，实现精细化领域语义问答。
* 长对话功能支持：引入会话窗口上下文缓存与历史记忆机制，使模型能够在多轮提问中保持一致性理解与跟进回答。

---

## 📄 许可证

本项目采用 MIT License，欢迎自由使用与二次开发。
