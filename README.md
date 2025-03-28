# Git Commits Extractor

一个用于提取和显示Git提交记录的工具。

## 功能

- 提取指定日期之后的 Git 提交记录
- 支持以表格或列表形式展示提交记录
- 自动识别当前用户的 Git 配置

## 安装

```bash
pip install git-commits-extractor
```

## 使用方法

```bash
git-commits-extractor --help
```

## 使用

在命令行中运行以下命令来提取 Git 提交记录：

```bash
python -m src.git_commits_extractor.main --repo-path /path/to/your/repo --since YYYY-MM-DD --format table
```

- `--repo-path`: 指定 Git 仓库的路径，默认为当前工作目录。
- `--since`: 可选参数，指定提取从该日期之后的提交记录，格式为 `YYYY-MM-DD`。
- `--format`: 输出格式，支持 `table` 或 `list`，默认为 `table`。

## 贡献

欢迎提交问题和功能请求，或直接提交代码贡献。

## 许可证

该项目采用 MIT 许可证，详细信息请参阅 LICENSE 文件。