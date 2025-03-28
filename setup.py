from setuptools import setup, find_packages
import os

# 处理README.md可能不存在的情况
try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "A tool to extract and display Git commit records."

setup(
    name="git-commits-extractor",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to extract and display Git commit records.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/git-commits-extractor",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "GitPython",
        "typer",
        "rich",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    # 添加入口点配置
    entry_points={
        "console_scripts": [
            "git-commits-extractor=git_commits_extractor.main:app",
        ],
    },
)
