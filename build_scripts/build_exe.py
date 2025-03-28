import os
import sys
import subprocess
import platform


def build_executable():
    # 获取输出目录
    dist_path = os.path.join(os.path.dirname(__file__), "../dist")
    # 获取主程序路径
    main_path = os.path.join(
        os.path.dirname(__file__), "../src/git_commits_extractor/main.py"
    )

    # 设置基本 PyInstaller 命令
    pyinstaller_command = [
        "venv/bin/pyinstaller",
    ]

    # 检查是否为macOS系统
    if platform.system() == "Darwin":
        # macOS特定选项
        pyinstaller_command.extend(
            [
                "--onefile",  # 生成单个可执行文件
                "--name",
                "git-commits-extractor",
                "--distpath",
                dist_path,
                # macOS特定选项
                "--osx-bundle-identifier",
                "com.gitcommitsextractor",
                # 如果需要针对特定架构构建，取消下面注释并选择一个
                # '--target-architecture', 'x86_64',  # 针对Intel芯片
                # '--target-architecture', 'arm64',   # 针对Apple Silicon
                # '--target-architecture', 'universal2', # 通用二进制(Intel和Apple Silicon)
            ]
        )

        # 可选：创建.app包（如果是GUI应用则启用此选项）
        # pyinstaller_command.append('--windowed')

        print("为macOS系统构建可执行文件...")
    else:
        # 其他系统使用原始选项
        pyinstaller_command.extend(
            [
                "--onefile",
                "--name",
                "git-commits-extractor",
                "--distpath",
                dist_path,
            ]
        )

    # 添加主程序路径
    pyinstaller_command.append(main_path)

    # 执行 PyInstaller 命令
    try:
        subprocess.run(pyinstaller_command, check=True)
        print("打包成功！可执行文件已生成在 dist 目录中。")

        if platform.system() == "Darwin":
            print("macOS可执行文件已创建。")
            # 设置可执行权限
            executable_path = os.path.join(dist_path, "git-commits-extractor")
            if os.path.exists(executable_path):
                os.chmod(executable_path, 0o755)
                print(f"已设置可执行权限: {executable_path}")
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}", file=sys.stderr)


if __name__ == "__main__":
    build_executable()
