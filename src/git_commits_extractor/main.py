import git
import os
import sys  # 添加sys模块导入
import argparse
import openai
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.status import Status
from typing import List, Dict, Any

# 初始化Rich控制台
console = Console()


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Git提交记录提取工具")
    parser.add_argument(
        "--since",
        type=str,
        help="提取从该日期之后的提交 (格式: YYYY-MM-DD)",
        default=None,
    )
    parser.add_argument(
        "--repo-path", type=str, help="Git仓库路径", default=os.getcwd()
    )
    parser.add_argument(
        "--format",
        type=str,
        help="输出格式: table, list",
        default="table",
        choices=["table", "list"],
    )
    parser.add_argument(
        "--extract-tasks",
        action="store_true",
        help="从提交信息中提取任务记录",
    )
    parser.add_argument(
        "--openai-api-key",
        type=str,
        help="OpenAI API密钥，用于任务提取。不提供时将尝试从环境变量OPENAI_API_KEY获取",
        default=None,
    )
    parser.add_argument(
        "--model",
        type=str,
        help="使用的OpenAI模型名称",
        default="gpt-4o-mini",
    )
    return parser.parse_args()


def display_as_table(commits):
    """以表格形式展示提交记录"""
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("提交哈希", style="dim")
    table.add_column("日期", style="cyan")
    table.add_column("提交信息", style="green")

    for commit in commits:
        commit_hash = commit.hexsha[:8]  # 简短哈希
        date = commit.authored_datetime.strftime("%Y-%m-%d %H:%M")
        message = commit.message.strip().split("\n")[0]  # 第一行

        table.add_row(commit_hash, date, message)

    console.print(table)


def extract_tasks_using_openai(
    commits: List[git.Commit], model: str
) -> List[Dict[str, Any]]:
    """使用OpenAI LLM分析提交记录并提取任务"""
    if not commits:
        return []

    try:
        # 构建提交信息文本
        commit_texts = []
        for commit in commits:
            date = commit.authored_datetime.strftime("%Y-%m-%d %H:%M")
            message = commit.message.strip()
            commit_texts.append(f"Date: {date}\nCommit message:\n{message}\n")

        all_commits = "\n---\n".join(commit_texts)

        # 构建增强版英文提示词，要求更详细的任务分解
        prompt = f"""
I need you to analyze the following Git commit messages and extract a comprehensive and detailed task breakdown.

For each identified work area:
1. Create a main task with a clear, descriptive title
2. Break down the task into detailed subtasks that explain specific components of the work
3. Include implementation details, technical considerations, or challenges addressed
4. Identify dependencies between tasks where visible
5. Ensure the task breakdown is granular enough to serve as documentation of the work performed

Present the tasks in chronological order when possible. Combine related commits into cohesive tasks rather than listing each commit separately.

Please return the result in JSON format, as follows:
[
  {{
    "task": "Detailed task name/title",
    "details": [
      "Specific implementation detail 1",
      "Technical component addressed 2",
      "Challenge overcome 3",
      "Design decision made 4",
      "Feature functionality 5"
    ],
    "date": "The most recent commit date related to this task"
  }},
  ...
]

Here are the commit messages to analyze:
{all_commits}
"""

        with Status("[bold yellow]正在使用AI分析提交记录...", console=console):
            # 调用OpenAI API
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional work task analysis assistant specialized in software development. Your expertise is breaking down Git commit histories into detailed, meaningful work tasks with comprehensive subtasks. Focus on providing granular technical details that effectively document the work performed.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,  # 降低温度以获得更一致的详细输出
                response_format={"type": "json_object"},
            )

            # 解析响应
            import json

            try:
                content = response.choices[0].message.content
                result = json.loads(content)

                # 确保结果是列表格式
                if isinstance(result, dict) and "tasks" in result:
                    tasks = result["tasks"]
                elif not isinstance(result, list):
                    tasks = []
                else:
                    tasks = result

                # 转换为我们的任务格式
                formatted_tasks = []
                for task_item in tasks:
                    formatted_task = {
                        "description": task_item.get("task", "未命名任务"),
                        "subtasks": task_item.get("details", []),
                        "date": task_item.get("date", ""),
                    }
                    formatted_tasks.append(formatted_task)

                return formatted_tasks
            except json.JSONDecodeError:
                console.print("[bold red]AI返回的内容无法解析为JSON格式[/bold red]")
                return []

    except Exception as e:
        console.print(f"[bold red]调用OpenAI API时发生错误: {str(e)}[/bold red]")
        return []


def display_tasks(tasks):
    """展示从提交信息中提取的任务"""
    if not tasks:
        console.print("[yellow]没有找到任务记录[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("日期", style="cyan")
    table.add_column("任务", style="green")
    table.add_column("详细信息", style="dim")

    for task in tasks:
        date = task.get("date", "")
        description = task["description"]

        # 合并子任务为一个字符串
        subtasks_str = "\n".join([f"• {subtask}" for subtask in task["subtasks"]])

        table.add_row(date, description, subtasks_str)

    console.print(table)


def display_as_list(commits):
    """以列表形式展示提交记录"""
    for i, commit in enumerate(commits, 1):
        panel_content = f"[bold cyan]提交哈希:[/bold cyan] {commit.hexsha}\n"
        panel_content += f"[bold cyan]作者:[/bold cyan] {commit.author.name}\n"
        panel_content += f"[bold cyan]日期:[/bold cyan] {commit.authored_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n"
        panel_content += f"[bold cyan]提交信息:[/bold cyan]\n{commit.message.strip()}"

        panel = Panel(
            panel_content,
            title=f"[bold]提交 #{i}[/bold]",
            subtitle=f"[dim]{commit.hexsha[:8]}[/dim]",
            border_style="green",
        )
        console.print(panel)

        # 如果不是最后一个提交，添加分隔符
        if i < len(commits):
            console.print("")


def main():
    """
    提取并展示当前用户的Git提交记录
    """
    args = parse_args()

    # 设置OpenAI API密钥
    if args.extract_tasks:
        api_key = args.openai_api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            console.print(
                "[bold red]错误: 未提供OpenAI API密钥。请通过--openai-api-key参数提供或设置OPENAI_API_KEY环境变量[/bold red]"
            )
            return 1
        os.environ["OPENAI_API_KEY"] = api_key

    with Status("[bold green]正在分析Git提交记录...", console=console) as status:
        try:
            # 获取仓库
            repo = git.Repo(args.repo_path)

            # 获取当前用户的邮箱
            author_email = repo.config_reader().get_value("user", "email")
            console.print(
                f"当前用户: [bold]{repo.config_reader().get_value('user', 'name')}[/bold] <{author_email}>"
            )

            # 设置日期过滤条件
            date_filter = None
            if args.since:
                try:
                    date_filter = datetime.strptime(args.since, "%Y-%m-%d")
                    console.print(f"过滤日期: [bold cyan]{args.since}[/bold cyan] 之后")
                except ValueError:
                    console.print(
                        "[bold red]日期格式错误，请使用YYYY-MM-DD格式[/bold red]"
                    )
                    return 1

            # 获取所有提交
            commits = list(repo.iter_commits())

            # 筛选出当前用户的提交，并根据日期过滤
            my_commits = []
            for commit in commits:
                if commit.author.email == author_email:
                    if (
                        date_filter is None
                        or commit.authored_datetime.replace(tzinfo=None) >= date_filter
                    ):
                        my_commits.append(commit)

            console.print(f"找到 [bold green]{len(my_commits)}[/bold green] 条提交记录")

        except git.exc.InvalidGitRepositoryError:
            console.print(
                f"[bold red]错误: {args.repo_path} 不是一个有效的Git仓库[/bold red]"
            )
            return 1
        except Exception as e:
            console.print(f"[bold red]发生错误: {str(e)}[/bold red]")
            return 1

    # 展示提交记录
    if not my_commits:
        console.print("[yellow]没有找到符合条件的提交记录[/yellow]")
        return 0

    if args.extract_tasks:
        # 使用OpenAI提取并展示任务
        tasks = extract_tasks_using_openai(my_commits, args.model)
        display_tasks(tasks)
    else:
        # 按原有方式展示提交记录
        if args.format == "table":
            display_as_table(my_commits)
        else:
            display_as_list(my_commits)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # 使用sys.exit代替exit
