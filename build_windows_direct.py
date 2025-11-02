#!/usr/bin/env python3
"""
VIP追剧神器 - Windows直接构建安卓APK工具
提供多种Windows环境下的构建方案
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

class WindowsAndroidBuilder:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.build_dir = self.project_dir / "android_build"
        self.dist_dir = self.project_dir / "android_dist"
        
    def check_environment(self):
        """检查Windows环境"""
        print("🔍 检查Windows构建环境...")
        
        # 检查Python版本
        if sys.version_info < (3, 7):
            print("❌ 需要Python 3.7或更高版本")
            return False
            
        # 检查Java
        try:
            result = subprocess.run(["java", "-version"], capture_output=True, text=True)
            print("✅ Java已安装")
        except FileNotFoundError:
            print("⚠️  未检测到Java，建议安装JDK 8或11")
            print("   下载地址: https://adoptopenjdk.net/")
            
        # 检查Android SDK
        android_sdk = os.environ.get("ANDROID_SDK_ROOT") or os.environ.get("ANDROID_HOME")
        if not android_sdk:
            print("⚠️  未检测到Android SDK环境变量")
            print("   建议安装Android Studio或SDK命令行工具")
            
        return True
        
    def method1_python_android(self):
        """方法1: 使用python-for-android直接构建"""
        print("\n📱 方法1: 使用python-for-android构建")
        print("=" * 50)
        
        try:
            # 安装python-for-android
            print("正在安装python-for-android...")
            subprocess.run([sys.executable, "-m", "pip", "install", "python-for-android"], check=True)
            
            # 创建构建目录
            self.build_dir.mkdir(exist_ok=True)
            self.dist_dir.mkdir(exist_ok=True)
            
            # 准备构建命令
            build_cmd = [
                sys.executable, "-m", "pythonforandroid.toolchain",
                "apk", "--debug",
                "--private", str(self.project_dir),
                "--package", "org.vipfree.vipzhuiqi",
                "--name", "VIP追剧神器",
                "--version", "1.0",
                "--bootstrap", "sdl2",
                "--requirements", "python3,kivy,requests,Pillow",
                "--arch", "arm64-v8a",
                "--dist-name", "vipzhuiqi",
                "--local-recipes", str(self.project_dir / "recipes"),
            ]
            
            print("执行构建命令...")
            print(" ".join(build_cmd))
            
            # 运行构建
            result = subprocess.run(build_cmd, cwd=self.build_dir)
            
            if result.returncode == 0:
                print("✅ 构建成功！")
                self.find_apk_files()
            else:
                print("❌ 构建失败")
                
        except subprocess.CalledProcessError as e:
            print(f"❌ 安装失败: {e}")
            return False
        except Exception as e:
            print(f"❌ 错误: {e}")
            return False
            
    def method2_kivy_installer(self):
        """方法2: 使用Kivy官方安装器"""
        print("\n📱 方法2: 使用Kivy官方工具链")
        print("=" * 50)
        
        print("正在下载Kivy Android工具链...")
        
        # 创建工具目录
        tools_dir = self.project_dir / "kivy_android_tools"
        tools_dir.mkdir(exist_ok=True)
        
        # 下载Kivy Android工具
        tools_url = "https://github.com/kivy/kivy-android-tools/archive/refs/heads/main.zip"
        tools_zip = tools_dir / "kivy-tools.zip"
        
        try:
            print("下载Kivy Android工具...")
            subprocess.run([
                "powershell", "-Command",
                f"Invoke-WebRequest -Uri '{tools_url}' -OutFile '{tools_zip}'"
            ], check=True)
            
            print("解压工具...")
            subprocess.run([
                "powershell", "-Command",
                f"Expand-Archive -Path '{tools_zip}' -DestinationPath '{tools_dir}' -Force"
            ], check=True)
            
            print("✅ Kivy Android工具下载完成")
            print("📁 工具位置:", tools_dir)
            print("⚠️  需要手动配置和使用，请参考工具文档")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 下载失败: {e}")
            return False
            
    def method3_cloud_build(self):
        """方法3: 云构建服务"""
        print("\n☁️ 方法3: 使用云构建服务")
        print("=" * 50)
        
        services = [
            {
                "name": "GitHub Actions",
                "description": "免费的CI/CD服务，支持Android构建",
                "setup": "创建.github/workflows/android-build.yml文件"
            },
            {
                "name": "GitLab CI",
                "description": "集成CI/CD平台",
                "setup": "创建.gitlab-ci.yml文件"
            },
            {
                "name": "Travis CI",
                "description": "云CI服务",
                "setup": "创建.travis.yml文件"
            }
        ]
        
        print("推荐的云构建服务:")
        for i, service in enumerate(services, 1):
            print(f"{i}. {service['name']}: {service['description']}")
            print(f"   设置方法: {service['setup']}")
            print()
            
        print("✅ 我将为您创建GitHub Actions工作流文件")
        self.create_github_actions_workflow()
        
    def create_github_actions_workflow(self):
        """创建GitHub Actions工作流"""
        workflow_dir = self.project_dir / ".github" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_content = """
name: Build Android APK

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build-android:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r android_requirements.txt
        
    - name: Install Buildozer
      run: |
        sudo apt update
        sudo apt install -y python3-pip openjdk-8-jdk git zip unzip
        pip install buildozer
        
    - name: Build APK
      run: |
        buildozer android debug
        
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: android-apk
        path: bin/*.apk
        
    - name: Upload to Release
      if: startsWith(github.ref, 'refs/tags/')
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        draft: false
        prerelease: false
"""
        
        workflow_file = workflow_dir / "android-build.yml"
        workflow_file.write_text(workflow_content.strip())
        
        print(f"✅ GitHub Actions工作流已创建: {workflow_file}")
        print("📋 使用方法:")
        print("1. 将代码推送到GitHub仓库")
        print("2. GitHub Actions将自动构建APK")
        print("3. 在Actions标签页下载构建的APK文件")
        
    def method4_docker_build(self):
        """方法4: 使用Docker容器构建"""
        print("\n🐳 方法4: 使用Docker容器构建")
        print("=" * 50)
        
        # 创建Dockerfile
        dockerfile_content = """
FROM ubuntu:20.04

# 避免交互式配置
ENV DEBIAN_FRONTEND=noninteractive

# 安装基础依赖
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    openjdk-8-jdk \
    git \
    zip \
    unzip \
    wget \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# 安装buildozer
RUN pip3 install buildozer

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . /app/

# 安装Python依赖
RUN pip3 install -r android_requirements.txt

# 构建命令
CMD ["buildozer", "android", "debug"]
"""
        
        dockerfile = self.project_dir / "Dockerfile.android"
        dockerfile.write_text(dockerfile_content.strip())
        
        print("✅ Dockerfile已创建")
        print("🚀 使用方法:")
        print("1. 安装Docker Desktop for Windows")
        print("2. 构建Docker镜像:")
        print(f"   docker build -f {dockerfile} -t vip-android-build .")
        print("3. 运行容器构建APK:")
        print("   docker run -v ${PWD}/output:/app/bin vip-android-build")
        
    def find_apk_files(self):
        """查找生成的APK文件"""
        print("\n🔍 查找APK文件...")
        
        apk_files = []
        for pattern in ["*.apk", "*/bin/*.apk", "*/dist/*.apk"]:
            apk_files.extend(self.project_dir.glob(pattern))
            
        if apk_files:
            print("✅ 找到APK文件:")
            for apk in apk_files:
                print(f"   📱 {apk}")
        else:
            print("⚠️  未找到APK文件")
            
    def run(self):
        """主运行函数"""
        print("🚀 VIP追剧神器 - Windows安卓APK构建工具")
        print("=" * 60)
        
        # 检查环境
        if not self.check_environment():
            return
            
        print("\n📋 可用的构建方法:")
        print("1. python-for-android (直接构建)")
        print("2. Kivy官方工具链")
        print("3. 云构建服务 (GitHub Actions)")
        print("4. Docker容器构建")
        print("5. 退出")
        
        choice = input("\n请选择构建方法 (1-5): ").strip()
        
        if choice == "1":
            self.method1_python_android()
        elif choice == "2":
            self.method2_kivy_installer()
        elif choice == "3":
            self.method3_cloud_build()
        elif choice == "4":
            self.method4_docker_build()
        elif choice == "5":
            print("👋 再见！")
        else:
            print("❌ 无效选择")

if __name__ == "__main__":
    builder = WindowsAndroidBuilder()
    builder.run()