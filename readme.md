# VIP 视频解析工具

一个简单易用的 VIP 视频解析工具，支持多个解析接口，让您免费观看 VIP 视频内容。

## 功能特点

- 🎥 支持多个解析接口，自动切换
- 🖥️ 简洁易用的图形界面
- 🔄 自动解析视频链接
- 🚀 快速播放，无需等待
- 🛡️ 安全提示，防止诈骗

## 安装说明

### 环境要求

- Python 3.7+
- Tkinter (通常随 Python 一起安装)

### 安装步骤

1. 克隆本仓库
   ```bash
   git clone [仓库URL]
   cd vip-free
   ```

2. 创建并激活虚拟环境（推荐）
   ```bash
   # 使用 uv（推荐）
   uv venv
   # Windows
   .\.venv\Scripts\activate
   # Unix/macOS
   source .venv/bin/activate
   ```

3. 安装依赖
   ```bash
   uv sync  # 如果使用 uv
   # 或者
   pip install -r requirements.txt
   ```

## 使用方法

1. 运行程序
   ```bash
   python app.py
   ```

2. 在输入框中粘贴 VIP 视频链接

3. 选择解析接口（默认为接口1）

4. 点击"解析播放"按钮

5. 等待解析完成，视频将在默认浏览器中打开

## 支持的视频平台

- 腾讯视频
- 爱奇艺
- 优酷

## 常见问题

### 1. 解析失败怎么办？
- 尝试切换其他解析接口
- 检查网络连接是否正常
- 确保视频链接正确

### 2. 程序无法启动
- 确保已安装 Python 3.7 或更高版本
- 确保已安装所有依赖项
- 检查是否已激活虚拟环境
