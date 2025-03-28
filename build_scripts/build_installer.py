import os
import subprocess
import sys
import platform
import shutil


def create_installer():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 设置安装包的名称和版本
    package_name = "git-commits-extractor"
    version = "0.1.0"

    # 使用 PyInstaller 创建可执行文件
    try:
        subprocess.run([sys.executable, "build_scripts/build_exe.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"创建可执行文件时出错: {e}")
        return

    # 检查是否为macOS
    if platform.system() == "Darwin":
        print("为macOS创建安装包...")
        dist_dir = os.path.join(current_dir, "..", "dist")
        executable_path = os.path.join(dist_dir, package_name)

        # 确保可执行文件存在
        if not os.path.exists(executable_path):
            print(f"错误: 可执行文件未找到: {executable_path}")
            return

        # 创建DMG安装包(需要安装create-dmg工具)
        try:
            # 可选：如果使用create-dmg工具创建DMG
            # dmg_command = [
            #     "create-dmg",
            #     "--volname", f"{package_name} {version}",
            #     "--app-drop-link", "450", "170",
            #     executable_path,
            #     os.path.join(dist_dir, f"{package_name}-{version}.dmg")
            # ]
            # subprocess.run(dmg_command, check=True)
            # print(f"macOS DMG 安装包已创建: dist/{package_name}-{version}.dmg")

            # 创建压缩包作为替代
            zip_path = os.path.join(dist_dir, f"{package_name}-{version}-macos.zip")
            shutil.make_archive(zip_path[:-4], "zip", dist_dir, package_name)
            print(f"macOS 压缩包已创建: {zip_path}")

        except Exception as e:
            print(f"创建macOS安装包时出错: {e}")
    else:
        # 其他平台使用wheel包
        try:
            subprocess.run(["python", "setup.py", "bdist_wheel"], check=True)
            print(f"安装包已创建: dist/{package_name}-{version}-py3-none-any.whl")
        except subprocess.CalledProcessError as e:
            print(f"创建安装包时出错: {e}")


if __name__ == "__main__":
    create_installer()
