import os
import sys
import subprocess

def build_exe():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建命令
    cmd = [
        'pyinstaller',
        '--noconfirm',           # 不需要确认覆盖
        '--onedir',              # 打包到一个目录
        '--windowed',            # Windows下禁用控制台
        '--name', 'VIP追剧神器',  # 应用名称
        '--icon', 'NONE',        # 没有图标文件
        '--add-data', f'asset;asset',  # 添加资源文件
        'app.py'
    ]
    
    # 运行打包命令
    print("开始打包应用...")
    result = subprocess.run(cmd, cwd=current_dir)
    
    if result.returncode == 0:
        print("打包完成！")
        print("可执行文件位置: dist/VIP追剧神器/")
    else:
        print("打包失败，请检查错误信息。")

if __name__ == "__main__":
    build_exe()