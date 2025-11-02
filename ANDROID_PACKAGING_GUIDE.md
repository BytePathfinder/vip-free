# VIP追剧神器 - 安卓版本打包指南

## 🎯 概述

本指南提供了多种在Windows环境下构建安卓APK的方法，无需使用WSL。

## 📋 文件结构

```
vip-free/
├── android_app.py              # 安卓版本主应用
├── buildozer.spec              # 构建配置文件
├── android_requirements.txt    # 安卓依赖
├── build_windows_direct.py     # Windows直接构建工具
├── build_docker_windows.bat    # Docker构建脚本
├── Dockerfile.android          # Docker构建镜像
├── .github/workflows/          # GitHub Actions工作流
│   └── android-build.yml
└── asset/                      # 资源文件
    └── qr_wechat.png
```

## 🚀 快速开始

### 1. 环境准备

确保已安装以下软件：
- ✅ Python 3.7+
- ✅ Git
- ✅ Java JDK 8 或 11
- ✅ Docker Desktop (可选，但推荐)

### 2. 安装依赖

```bash
# 安装Python依赖
pip install -r android_requirements.txt

# 测试应用
python android_app.py
```

### 3. 选择构建方法

## 📱 构建方法

### 方法0: Windows直接构建工具 ⭐ 推荐

#### 选项A: 使用Windows构建工具
```bash
# 运行Windows直接构建工具
python build_windows_direct.py
```

按照提示选择构建方法：
1. **python-for-android** - 直接构建
2. **Kivy官方工具链** - 下载官方工具
3. **云构建服务** - 使用GitHub Actions (推荐)
4. **Docker容器构建** - 使用Docker

#### 选项B: 使用Docker构建 (最推荐)
```bash
# 运行Docker构建脚本
build_docker_windows.bat
```

按照菜单选择：
- **1. Debug构建** - 开发版本
- **2. Release构建** - 发布版本
- **3. 构建并运行容器** - 交互模式
- **4. 仅构建镜像** - 只构建不运行

#### 选项C: 使用GitHub Actions (零配置)
1. **创建GitHub仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <你的GitHub仓库地址>
   git push -u origin main
   ```

2. **自动构建**
   - 推送代码后，GitHub Actions会自动开始构建
   - 在GitHub的Actions页面查看构建进度
   - 构建完成后在Artifacts中下载APK

3. **手动触发构建**
   - 访问GitHub仓库的Actions页面
   - 选择"Build Android APK"工作流
   - 点击"Run workflow"手动触发构建

### 方法1: python-for-android直接构建

```bash
# 安装python-for-android
pip install python-for-android

# 构建APK (需要Linux环境)
p4a apk --private . --package org.vipfree.vipzhuiqi \
  --name "VIP追剧神器" --version 1.0 \
  --bootstrap sdl2 --requirements python3,kivy,requests,Pillow \
  --arch arm64-v8a
```

### 方法2: Docker容器构建

```bash
# 构建Docker镜像
docker build -f Dockerfile.android -t vip-android-build .

# 运行构建 (Debug版本)
docker run --rm -v ${PWD}/output:/app/bin vip-android-build

# 运行构建 (Release版本)
docker run --rm -v ${PWD}/output:/app/bin vip-android-build release

# 交互模式
docker run -it --rm -v ${PWD}/output:/app/bin vip-android-build
```

### 方法3: 云构建服务

#### GitHub Actions (已配置)
- ✅ 零配置，推送即构建
- ✅ 自动缓存，加速构建
- ✅ 支持Debug和Release
- ✅ 自动发布功能

#### 其他CI/CD服务
- **GitLab CI** - 创建`.gitlab-ci.yml`
- **Travis CI** - 创建`.travis.yml`
- **Azure DevOps** - 使用Azure Pipelines

## 📦 获取APK文件

构建完成后，APK文件位置：

| 构建方法 | APK位置 | 获取方式 |
|---------|---------|----------|
| Docker | `output/*.apk` | 本地文件夹 |
| GitHub Actions | Artifacts | GitHub页面下载 |
| python-for-android | `dist/*.apk` | 本地构建 |

## 🔧 配置说明

### buildozer.spec重要配置

```ini
[app]
title = VIP追剧神器
package.name = vipzhuiqi
package.domain = org.vipfree
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,requests,Pillow
orientation = portrait
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 30
android.minapi = 21
android.ndk = 21.4.7075529
android.archs = arm64-v8a, armeabi-v7a
```

### 安卓权限配置

```ini
android.permissions = INTERNET,ACCESS_NETWORK_STATE
```

### 应用图标和启动图

将图标文件放入项目目录：
- `icon.png` - 应用图标 (512x512)
- `presplash.png` - 启动画面 (1080x1920)

在buildozer.spec中配置：
```ini
icon.filename = icon.png
presplash.filename = presplash.png
```

## 🎨 安卓版本特性

- 📱 **适配移动端** - 专为手机屏幕设计
- 👆 **触摸操作** - 支持手势操作
- 🔄 **响应式布局** - 自适应不同屏幕尺寸
- 📸 **二维码显示** - 保留二维码功能
- 🎨 **现代UI** - Material Design风格
- ⚡ **性能优化** - 针对移动设备优化

## ⚠️ 重要提醒

### 首次构建注意事项
- ⏱️ **构建时间**: 首次构建可能需要30分钟到2小时
- 📦 **下载大小**: 需要下载Android SDK、NDK等（约5GB）
- 💾 **存储空间**: 确保至少有10GB可用空间
- 🌐 **网络要求**: 需要稳定的网络连接

### 常见问题和解决方案

#### 1. 构建失败
```bash
# 清理构建缓存
docker system prune -a
# 或清理buildozer缓存
rm -rf .buildozer
```

#### 2. APK安装失败
- 确保在安卓设置中允许"未知来源"
- 检查APK是否与设备架构兼容
- 尝试卸载旧版本后重新安装

#### 3. 应用闪退
- 检查logcat日志：`adb logcat`
- 确保所有依赖项正确打包
- 验证权限配置是否正确

#### 4. 二维码不显示
- 确认asset文件正确打包
- 检查文件路径处理逻辑
- 验证图片格式和大小

## 🚀 高级功能

### 自动发布
GitHub Actions工作流支持自动发布：
1. 创建git标签：`git tag v1.0.0`
2. 推送标签：`git push origin v1.0.0`
3. 自动创建GitHub Release并上传APK

### 多架构支持
支持以下CPU架构：
- `arm64-v8a` - 新设备 (推荐)
- `armeabi-v7a` - 旧设备
- `x86_64` - Intel设备
- `x86` - 模拟器

### 签名配置
Release版本需要签名：
```ini
# 在buildozer.spec中配置
android.release_artifact = apk
android.sign = True
android.keystore_path = release.keystore
android.keystore_password = your_password
android.keystore_alias = your_alias
```

## 📞 技术支持

如果遇到问题：

1. **查看构建日志** - 详细的错误信息
2. **检查GitHub Issues** - 常见问题解答
3. **验证环境配置** - 确保所有依赖正确安装
4. **测试应用代码** - 先运行`python android_app.py`

## 📄 许可证

本项目采用开源许可证，详见项目根目录的LICENSE文件。

---

**最后更新**: 2024年11月
**构建工具版本**: Buildozer 1.5.0, Python-for-android 2023.09.17