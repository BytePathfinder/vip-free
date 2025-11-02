@echo off
REM VIP追剧神器 - Windows Docker构建脚本
REM 使用Docker容器在Windows下构建安卓APK

echo ==================================================
echo 📱 VIP追剧神器 - Windows Docker APK构建工具
echo ==================================================

REM 检查Docker是否安装
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未检测到Docker
    echo 📥 请安装Docker Desktop for Windows:
    echo    https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✅ Docker已安装

REM 检查Docker是否运行
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker服务未运行
    echo 🔧 请启动Docker Desktop
    pause
    exit /b 1
)

echo ✅ Docker服务运行正常

REM 显示Docker信息
echo 📋 Docker信息:
docker --version

:menu
echo.
echo 构建选项:
echo 1. Debug构建 (推荐)
echo 2. Release构建
echo 3. 构建并运行容器
echo 4. 仅构建镜像
echo 5. 退出
echo.

set /p choice=请选择 (1-5): 

if "%choice%"=="1" goto debug_build
if "%choice%"=="2" goto release_build
if "%choice%"=="3" goto build_and_run
if "%choice%"=="4" goto build_image_only
if "%choice%"=="5" goto end

echo ❌ 无效选择，请重新选择
goto menu

:debug_build
echo.
echo 🏗️  开始Debug构建...
docker build -f Dockerfile.android -t vip-zhuiqi-android .
docker run --rm -v %cd%\output:/app/bin vip-zhuiqi-android

echo.
echo ✅ Debug构建完成!
echo 📱 检查output目录中的APK文件
if exist output\*.apk (
    echo ✅ APK文件已生成:
    dir output\*.apk
) else (
    echo ⚠️  未找到APK文件，请检查构建日志
)
pause
goto menu

:release_build
echo.
echo 🏗️  开始Release构建...
docker build -f Dockerfile.android -t vip-zhuiqi-android .
docker run --rm -v %cd%\output:/app/bin vip-zhuiqi-android release

echo.
echo ✅ Release构建完成!
echo 📱 检查output目录中的APK文件
if exist output\*.apk (
    echo ✅ APK文件已生成:
    dir output\*.apk
) else (
    echo ⚠️  未找到APK文件，请检查构建日志
)
pause
goto menu

:build_and_run
echo.
echo 🐳 构建镜像并运行容器...
docker build -f Dockerfile.android -t vip-zhuiqi-android .
echo ✅ 镜像构建完成

echo.
echo 🚀 运行构建容器...
docker run -it --rm -v %cd%\output:/app/bin vip-zhuiqi-android

echo.
echo ✅ 容器运行完成!
pause
goto menu

:build_image_only
echo.
echo 🐳 仅构建Docker镜像...
docker build -f Dockerfile.android -t vip-zhuiqi-android .
echo ✅ 镜像构建完成!
pause
goto menu

:end
echo 👋 再见!
pause