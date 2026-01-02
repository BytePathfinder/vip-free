# UV 工具使用速查表

## 1. 安装 UV

```bash
# 使用官方安装脚本
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或通过 pip 安装
pip install uv

# 更新 UV
uv self update
```

## 2. 项目初始化

```bash
# 创建项目目录
mkdir myproject
cd myproject

# 初始化项目（创建 pyproject.toml）
uv init
```

## 3. 依赖管理

### 添加依赖
```bash
# 添加主依赖
uv add requests

# 添加开发依赖
uv add --dev pytest

# 添加到特定组
uv add --group test pytest-cov

# 安装特定版本
uv add "package==1.2.3"

# 从 requirements.txt 安装
uv pip install -r requirements.txt
```

### 更新与移除依赖
```bash
# 更新所有依赖
uv pip install --upgrade -r requirements.txt

# 更新特定包
uv pip install --upgrade package_name

# 移除包
uv remove package_name
```

## 4. 虚拟环境管理

```bash
# 创建虚拟环境
uv venv

# 指定 Python 版本
uv venv --python 3.10

# 激活虚拟环境
# Windows
.\\.venv\Scripts\activate
# Unix/macOS
source .venv/bin/activate

# 退出虚拟环境
deactivate
```

## 5. 运行项目

```bash
# 运行 Python 脚本
uv run python app.py

# 运行模块
uv run -m mymodule

# 运行命令行工具
uv run pytest
```

## 6. 依赖同步与锁定

```bash
# 同步项目依赖
uv sync

# 生成 requirements.txt
uv pip freeze > requirements.txt

# 检查依赖冲突
uv pip check

# 显示依赖树
uv pip list --tree
```

## 7. 项目发布

```bash
# 安装构建工具
uv add --dev build

# 构建分发包
uv run python -m build

# 发布到 PyPI
uv add --dev twine
uv run python -m twine upload dist/*
```

## 8. 常用工作流

### 开发新功能
```bash
# 1. 创建并切换到新分支
git checkout -b feature/new-feature

# 2. 添加新依赖
uv add new-package

# 3. 开发代码
# ...

# 4. 运行测试
uv run pytest

# 5. 提交更改
git add .
git commit -m "Add new feature"
```

### 协作开发
```bash
# 1. 克隆仓库
git clone repo-url
cd repo

# 2. 创建并激活虚拟环境
uv venv
# Windows: .\.venv\Scripts\activate
# Unix/macOS: source .venv/bin/activate

# 3. 安装依赖
uv sync

# 4. 开始开发
# ...
```

## 9. 性能优化

```bash
# 使用并行安装加速
uv pip install --parallel package_name

# 使用本地缓存
uv pip install --cache-dir ~/.cache/uv package_name

# 设置环境变量
# 设置缓存目录
export UV_CACHE_DIR=~/.cache/uv
# 设置超时时间
export UV_HTTP_TIMEOUT=60
```

## 10. 常见问题

### 如何查看帮助？
```bash
uv --help
uv pip --help
uv add --help
```

### 如何查看已安装的包？
```bash
uv pip list
```

### 如何安装 Git 仓库中的包？
```bash
uv add git+https://github.com/user/repo.git
```

### 如何安装本地包？
```bash
uv add /path/to/your/package
```

---

> 提示：UV 是 pip 的快速替代品，大多数情况下可以将 `pip` 命令替换为 `uv pip` 使用。
