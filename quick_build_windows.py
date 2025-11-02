#!/usr/bin/env python3
"""
VIP追剧神器 - Windows快速构建工具
一键式安卓APK构建解决方案
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def print_banner():
    print("🚀" * 50)
    print("📱 VIP追剧神器 - Windows快速构建工具")
    print("🚀" * 50)

def check_docker():
    """检查Docker是否安装和运行"""
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            # 检查Docker是否正在运行
            result2 = subprocess.run(["docker", "info"], capture_output=True, text=True)
            return result2.returncode == 0
    except FileNotFoundError:
        return False
    return False

def install_docker():
    """引导用户安装Docker"""
    print("\n📦 Docker安装指南:")
    print("1. 访问: https://www.docker.com/products/docker-desktop")
    print("2. 下载Docker Desktop for Windows")
    print("3. 安装并启动Docker Desktop")
    print("4. 等待Docker完全启动（图标变绿色）")
    
    choice = input("\n是否现在打开Docker下载页面？(y/n): ").strip().lower()
    if choice == 'y':
        webbrowser.open("https://www.docker.com/products/docker-desktop")
    
    print("\n⚠️  安装完成后请重新运行本脚本")

def build_with_docker():
    """使用Docker构建"""
    print("\n🐳 使用Docker构建APK...")
    print("=" * 40)
    
    # 检查Docker
    if not check_docker():
        print("❌ Docker未安装或未运行")
        install_docker()
        return False
    
    print("✅ Docker运行正常")
    
    # 构建镜像
    print("📦 构建Docker镜像...")
    result = subprocess.run(["docker", "build", "-f", "Dockerfile.android", "-t", "vip-android", "."])
    if result.returncode != 0:
        print("❌ Docker镜像构建失败")
        return False
    
    print("✅ Docker镜像构建完成")
    
    # 运行构建
    print("🏗️  开始构建APK...")
    print("⚠️  首次构建可能需要30-60分钟，请耐心等待...")
    
    result = subprocess.run([
        "docker", "run", "--rm",
        "-v", f"{Path.cwd()}/output:/app/bin",
        "vip-android"
    ])
    
    if result.returncode == 0:
        print("\n🎉 APK构建成功！")
        
        # 检查输出文件
        output_dir = Path("output")
        if output_dir.exists():
            apk_files = list(output_dir.glob("*.apk"))
            if apk_files:
                print("\n📱 生成的APK文件:")
                for apk in apk_files:
                    print(f"   ✅ {apk.name}")
                    print(f"   📁 完整路径: {apk.absolute()}")
                
                print(f"\n💡 提示: APK文件已保存到: {output_dir.absolute()}")
                return True
            else:
                print("⚠️  未在output目录找到APK文件")
        else:
            print("⚠️  output目录不存在")
    else:
        print("\n❌ APK构建失败")
        print("💡 建议查看上面的错误信息，或尝试其他构建方法")
    
    return False

def setup_github_actions():
    """设置GitHub Actions"""
    print("\n☁️ 设置GitHub Actions自动构建...")
    print("=" * 40)
    
    # 检查是否已有Git仓库
    if not Path(".git").exists():
        print("⚠️  未检测到Git仓库")
        print("\n📋 GitHub设置步骤:")
        print("1. 访问 https://github.com/new 创建新仓库")
        print("2. 记住仓库名称（如：vip-zhuiqi）")
        print("3. 按以下步骤初始化本地仓库:")
        print()
        print("   git init")
        print("   git add .")
        print("   git commit -m 'Initial commit'")
        print("   git remote add origin https://github.com/你的用户名/仓库名.git")
        print("   git push -u origin main")
        print()
        
        choice = input("是否现在打开GitHub创建页面？(y/n): ").strip().lower()
        if choice == 'y':
            webbrowser.open("https://github.com/new")
        
        print("\n⚠️  创建仓库并推送代码后，GitHub Actions会自动构建APK")
        print("📱 构建完成后可在Actions页面下载APK文件")
    else:
        print("✅ 检测到Git仓库")
        print("\n📋 下一步:")
        print("1. 确保代码已提交: git add . && git commit -m 'Add android build'")
        print("2. 推送到GitHub: git push origin main")
        print("3. 访问GitHub仓库的Actions页面查看构建进度")
        print("4. 构建完成后下载APK文件")
        
        choice = input("\n是否现在打开GitHub Actions页面？(y/n): ").strip().lower()
        if choice == 'y':
            # 尝试获取远程仓库URL
            try:
                result = subprocess.run(["git", "remote", "get-url", "origin"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    repo_url = result.stdout.strip()
                    if repo_url.endswith('.git'):
                        repo_url = repo_url[:-4]
                    actions_url = f"{repo_url}/actions"
                    webbrowser.open(actions_url)
            except:
                webbrowser.open("https://github.com")

def show_menu():
    """显示主菜单"""
    print("\n📋 快速构建选项:")
    print("1. 🐳 Docker一键构建 (推荐)")
    print("2. ☁️ GitHub Actions自动构建")
    print("3. 📖 查看详细构建指南")
    print("4. 🧪 测试安卓应用")
    print("5. ❌ 退出")
    
    choice = input("\n请选择 (1-5): ").strip()
    return choice

def test_android_app():
    """测试安卓应用"""
    print("\n🧪 测试安卓应用...")
    result = subprocess.run([sys.executable, "android_app.py"])
    return result.returncode == 0

def main():
    """主函数"""
    print_banner()
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            success = build_with_docker()
            if success:
                print("\n🎉 恭喜！APK构建成功！")
                print("📱 您现在可以将APK文件安装到安卓手机上使用了")
            else:
                print("\n💡 构建失败，建议尝试GitHub Actions方法")
                
        elif choice == "2":
            setup_github_actions()
            
        elif choice == "3":
            print("\n📖 打开详细构建指南...")
            try:
                import webbrowser
                webbrowser.open("ANDROID_PACKAGING_GUIDE.md")
            except:
                print("📁 请查看 ANDROID_PACKAGING_GUIDE.md 文件")
                
        elif choice == "4":
            print("\n🧪 测试安卓应用代码...")
            if test_android_app():
                print("✅ 安卓应用代码正常！")
            else:
                print("❌ 安卓应用代码有问题，请检查错误信息")
                
        elif choice == "5":
            print("\n👋 感谢使用VIP追剧神器构建工具！")
            print("⭐ 如果本工具对您有帮助，请给个Star支持！")
            break
            
        else:
            print("❌ 无效选择，请重新选择")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("💡 请检查环境配置或查看详细指南")