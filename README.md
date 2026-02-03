# Git Commits Extractor

> Extract your Git commits and let AI summarize what you've been working on.

[中文](#中文) | [English](#english)

---

## 中文

从 Git 仓库提取提交记录，并使用 AI 自动生成任务总结。适合写周报、复盘工作内容。

### 快速开始

```bash
# 安装
pip install git-commits-extractor

# 查看本周提交
git-commits-extractor --since 2025-01-27

# 让 AI 帮你总结任务
git-commits-extractor --since 2025-01-01 --extract-tasks
```

### 主要功能

| 功能 | 说明 |
|------|------|
| 提交提取 | 按日期筛选，自动过滤当前用户的提交 |
| 多种格式 | 表格 `table` 或列表 `list` 展示 |
| AI 总结 | 调用 OpenAI 分析提交，提取任务清单 |

### 参数说明

```bash
git-commits-extractor [OPTIONS]

--repo-path PATH      # 仓库路径，默认当前目录
--since YYYY-MM-DD    # 起始日期
--format table|list   # 输出格式，默认 table
--extract-tasks       # 启用 AI 任务提取
--openai-api-key KEY  # OpenAI API 密钥（或设置环境变量 OPENAI_API_KEY）
--model MODEL         # 模型名称，默认 gpt-4o-mini
```

### 许可证

MIT

---

## English

Extract Git commits and let AI summarize your work. Perfect for writing weekly reports or reviewing what you've accomplished.

### Quick Start

```bash
# Install
pip install git-commits-extractor

# View this week's commits
git-commits-extractor --since 2025-01-27

# Let AI summarize your tasks
git-commits-extractor --since 2025-01-01 --extract-tasks
```

### Features

| Feature | Description |
|---------|-------------|
| Commit Extraction | Filter by date, auto-filter by current Git user |
| Multiple Formats | Display as `table` or `list` |
| AI Summary | Use OpenAI to analyze commits and extract task list |

### Options

```bash
git-commits-extractor [OPTIONS]

--repo-path PATH      # Repository path, defaults to current directory
--since YYYY-MM-DD    # Start date filter
--format table|list   # Output format, defaults to table
--extract-tasks       # Enable AI task extraction
--openai-api-key KEY  # OpenAI API key (or set OPENAI_API_KEY env var)
--model MODEL         # Model name, defaults to gpt-4o-mini
```

### License

MIT
