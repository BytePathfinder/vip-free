#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VIP追剧神器 - Android版本
使用Kivy框架开发的安卓应用
"""

import os
import sys
import webbrowser
from pathlib import Path
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import dp
from PIL import Image as PILImage
import requests
import threading

# 设置字体支持（确保中文显示正常）
def setup_fonts():
    # 尝试加载系统字体
    system_fonts = []
    # Windows系统常见中文字体路径
    if sys.platform.startswith('win'):
        font_paths = [
            r'C:\Windows\Fonts\simsun.ttc',      # 宋体
            r'C:\Windows\Fonts\simhei.ttf',      # 黑体
            r'C:\Windows\Fonts\msyh.ttc',        # 微软雅黑
            r'C:\Windows\Fonts\microsoftyahei.ttf',  # 微软雅黑
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                system_fonts.append(font_path)
                try:
                    font_name = os.path.basename(font_path).split('.')[0]
                    LabelBase.register(name=font_name, fn_regular=font_path)
                    print(f"✅ 加载字体: {font_name} - {font_path}")
                except Exception as e:
                    print(f"⚠️ 加载字体失败: {font_path} - {e}")
    
    return system_fonts

# 设置窗口属性
Window.size = (360, 640)
Window.clearcolor = (0.1, 0.1, 0.1, 1)
Window.fullscreen = False
Window.resizable = True

# 初始化字体
loaded_fonts = setup_fonts()
DEFAULT_FONT = None
if loaded_fonts:
    DEFAULT_FONT = os.path.basename(loaded_fonts[0]).split('.')[0]

class VipVideoApp(App):
    def build(self):
        self.title = 'VIP追剧神器'
        
        # 重新导入所需的布局类以避免作用域问题
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.scrollview import ScrollView
        
        # 主布局 - 添加ScrollView确保在小屏幕上可以滚动
        root_layout = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # 标题 - 添加字体设置
        title_config = {
            'text': 'VIP追剧神器',
            'font_size': dp(24),
            'size_hint_y': None,
            'height': dp(60),
            'color': (1, 0.8, 0.2, 1),
            'halign': 'center',
            'valign': 'middle'
        }
        
        # 如果有加载的字体，使用它
        if DEFAULT_FONT:
            title_config['font_name'] = DEFAULT_FONT
        
        title_label = Label(**title_config)
        main_layout.add_widget(title_label)
        
        # 平台按钮区域 - 修复GridLayout配置
        platforms_layout = GridLayout(
            cols=2, 
            spacing=dp(10), 
            size_hint_y=None,
            height=dp(220),  # 增加高度以确保所有按钮都能显示
            row_default_height=dp(65),  # 设置行高
            row_force_default=True      # 强制使用行高
        )
        
        # 定义平台
        platforms = [
            {"name": "腾讯视频", "color": (0.2, 0.6, 1, 1)},
            {"name": "爱奇艺", "color": (0.1, 0.8, 0.2, 1)},
            {"name": "优酷", "color": (1, 0.3, 0.3, 1)}
        ]
        
        # 创建平台按钮
        for platform in platforms:
            btn_config = {
                'text': platform["name"],
                'background_color': platform["color"],
                'font_size': dp(16),
                'size_hint_y': None,
                'height': dp(65),
                'halign': 'center',
                'valign': 'middle'
            }
            
            # 如果有加载的字体，使用它
            if DEFAULT_FONT:
                btn_config['font_name'] = DEFAULT_FONT
            
            btn = Button(**btn_config)
            btn.bind(on_press=self.on_platform_click)
            platforms_layout.add_widget(btn)
        
        main_layout.add_widget(platforms_layout)
        
        # 搜索平台区域
        search_label_config = {
            'text': '去找电影:',
            'font_size': dp(16),
            'size_hint_y': None,
            'height': dp(40),
            'color': (1, 1, 1, 1),
            'halign': 'left',
            'valign': 'middle'
        }
        if DEFAULT_FONT:
            search_label_config['font_name'] = DEFAULT_FONT
        search_label = Label(**search_label_config)
        main_layout.add_widget(search_label)
        
        # 平台快捷按钮
        quick_platforms_layout = GridLayout(
            cols=3, 
            spacing=dp(5), 
            size_hint_y=None,
            height=dp(50)
        )
        
        quick_platforms = [
            "爱奇艺",
            "腾讯视频",
            "优酷视频"
        ]
        
        for platform in quick_platforms:
            quick_btn_config = {
                'text': platform,
                'background_color': (0.6, 0.6, 0.6, 1),
                'font_size': dp(14),
                'size_hint_y': None,
                'height': dp(40),
                'halign': 'center',
                'valign': 'middle'
            }
            
            if DEFAULT_FONT:
                quick_btn_config['font_name'] = DEFAULT_FONT
            
            btn = Button(**quick_btn_config)
            btn.bind(on_press=self.on_platform_click)
            quick_platforms_layout.add_widget(btn)
        
        main_layout.add_widget(quick_platforms_layout)
        
        # 网址输入区域
        url_label_config = {
            'text': '输入网址:',
            'font_size': dp(16),
            'size_hint_y': None,
            'height': dp(40),
            'color': (1, 1, 1, 1),
            'halign': 'left',
            'valign': 'middle'
        }
        if DEFAULT_FONT:
            url_label_config['font_name'] = DEFAULT_FONT
        url_label = Label(**url_label_config)
        main_layout.add_widget(url_label)
        
        # 输入框和按钮
        url_input_layout = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(40))
        
        from kivy.uix.textinput import TextInput
        self.url_input = TextInput(
            text='',
            multiline=False,
            font_size=dp(14),
            size_hint_x=0.7
        )
        if DEFAULT_FONT:
            self.url_input.font_name = DEFAULT_FONT
        
        clear_btn = Button(
            text='清空',
            background_color=(0.8, 0.2, 0.2, 1),
            font_size=dp(14),
            size_hint_x=0.15
        )
        if DEFAULT_FONT:
            clear_btn.font_name = DEFAULT_FONT
        clear_btn.bind(on_press=self.clear_url_input)
        
        play_btn = Button(
            text='播放',
            background_color=(0.2, 0.8, 0.2, 1),
            font_size=dp(14),
            size_hint_x=0.15
        )
        if DEFAULT_FONT:
            play_btn.font_name = DEFAULT_FONT
        play_btn.bind(on_press=self.play_from_url)
        
        url_input_layout.add_widget(self.url_input)
        url_input_layout.add_widget(clear_btn)
        url_input_layout.add_widget(play_btn)
        main_layout.add_widget(url_input_layout)
        
        # 解析接口选择
        api_label_config = {
            'text': '解析接口:',
            'font_size': dp(16),
            'size_hint_y': None,
            'height': dp(40),
            'color': (1, 1, 1, 1),
            'halign': 'left',
            'valign': 'middle'
        }
        if DEFAULT_FONT:
            api_label_config['font_name'] = DEFAULT_FONT
        api_label = Label(**api_label_config)
        main_layout.add_widget(api_label)
        
        # 接口选择布局
        api_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(40))
        
        from kivy.uix.checkbox import CheckBox
        from kivy.uix.boxlayout import BoxLayout
        
        # 创建一个单选按钮组
        self.api_group = BoxLayout(orientation='horizontal', spacing=dp(20))
        
        # 存储单选按钮引用
        self.api_radios = []
        
        for i in range(1, 4):
            api_item_layout = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint=(None, 1))
            
            # 使用CheckBox作为单选按钮
            check_box = CheckBox(group='api', size_hint=(None, None), size=(dp(20), dp(20)))
            if i == 1:  # 默认选择第一个
                check_box.active = True
            
            # 保存引用以便后续获取选中项
            self.api_radios.append((i, check_box))
            
            radio_label_config = {
                'text': f'接口{i}',
                'font_size': dp(14),
                'color': (1, 1, 1, 1),
                'valign': 'middle'
            }
            if DEFAULT_FONT:
                radio_label_config['font_name'] = DEFAULT_FONT
            radio_label = Label(**radio_label_config)
            
            api_item_layout.add_widget(check_box)
            api_item_layout.add_widget(radio_label)
            self.api_group.add_widget(api_item_layout)
        
        api_layout.add_widget(self.api_group)
        main_layout.add_widget(api_layout)
        
        # 警告信息
        warning_label_config = {
            'text': '请勿相信播放页面的广告，保护好自己的钱袋子。',
            'font_size': dp(14),
            'size_hint_y': None,
            'height': dp(40),
            'color': (1, 0, 0, 1),
            'halign': 'center',
            'valign': 'middle'
        }
        if DEFAULT_FONT:
            warning_label_config['font_name'] = DEFAULT_FONT
        warning_label = Label(**warning_label_config)
        main_layout.add_widget(warning_label)
        
        # 功能按钮区域
        functions_layout = BoxLayout(
            orientation='vertical', 
            spacing=dp(10), 
            size_hint_y=None,
            height=dp(160)  # 增加高度
        )
        
        # 创建功能按钮的通用函数
        def create_function_button(text, color):
            btn_config = {
                'text': text,
                'background_color': color,
                'font_size': dp(16),
                'size_hint_y': None,
                'height': dp(50),
                'halign': 'center',
                'valign': 'middle'
            }
            
            # 如果有加载的字体，使用它
            if DEFAULT_FONT:
                btn_config['font_name'] = DEFAULT_FONT
            
            return Button(**btn_config)
        
        # 二维码按钮
        qr_btn = create_function_button('显示二维码', (0.8, 0.2, 0.8, 1))
        qr_btn.bind(on_press=self.show_qr_code)
        functions_layout.add_widget(qr_btn)
        
        # 关于按钮
        about_btn = create_function_button('关于应用', (0.6, 0.6, 0.6, 1))
        about_btn.bind(on_press=self.show_about)
        functions_layout.add_widget(about_btn)
        
        main_layout.add_widget(functions_layout)
        
        # 状态标签
        status_config = {
            'text': '欢迎使用VIP追剧神器',
            'font_size': dp(14),
            'size_hint_y': None,
            'height': dp(40),
            'color': (0.8, 0.8, 0.8, 1),
            'halign': 'center',
            'valign': 'middle'
        }
        
        # 如果有加载的字体，使用它
        if DEFAULT_FONT:
            status_config['font_name'] = DEFAULT_FONT
        
        self.status_label = Label(**status_config)
        main_layout.add_widget(self.status_label)
        
        # 将主布局添加到ScrollView中
        root_layout.add_widget(main_layout)
        
        return root_layout
    
    def on_platform_click(self, instance):
        """平台按钮点击事件"""
        platform_name = instance.text
        self.status_label.text = f'正在打开 {platform_name}...'
        
        # 模拟打开平台
        def open_platform():
            # 这里可以添加实际的视频平台链接
            platforms = {
                "腾讯视频": "https://v.qq.com",
                "爱奇艺": "https://www.iqiyi.com",
                "优酷": "https://www.youku.com",

            }
            
            url = platforms.get(platform_name, "https://www.baidu.com")
            try:
                webbrowser.open(url)
                self.status_label.text = f'已打开 {platform_name}'
            except Exception as e:
                self.status_label.text = f'打开失败: {str(e)}'
        
        # 在新线程中打开，避免阻塞UI
        threading.Thread(target=open_platform, daemon=True).start()
    
    def show_qr_code(self, instance):
        """显示二维码"""
        self.status_label.text = '正在加载二维码...'
        
        # 创建二维码显示窗口
        qr_window = BoxLayout(orientation='vertical', padding=dp(20))
        
        # 标题
        title_config = {
            'text': '扫码关注公众号',
            'font_size': dp(20),
            'size_hint_y': None,
            'height': dp(40),
            'color': (1, 1, 1, 1),
            'halign': 'center',
            'valign': 'middle'
        }
        
        # 如果有加载的字体，使用它
        if DEFAULT_FONT:
            title_config['font_name'] = DEFAULT_FONT
        
        title = Label(**title_config)
        qr_window.add_widget(title)
        
        try:
            # 加载二维码图片
            qr_path = self.get_qr_path()
            
            if os.path.exists(qr_path):
                # 调整图片大小
                img = PILImage.open(qr_path)
                img = img.resize((250, 250), PILImage.Resampling.LANCZOS)
                
                # 保存调整后的图片
                temp_path = os.path.join(os.path.dirname(qr_path), "qr_temp.png")
                img.save(temp_path)
                
                # 显示图片
                qr_image = Image(
                    source=temp_path,
                    size_hint=(None, None),
                    size=(dp(250), dp(250)),
                    pos_hint={'center_x': 0.5}
                )
                qr_window.add_widget(qr_image)
            else:
                # 显示错误信息
                error_config = {
                    'text': '二维码加载失败',
                    'font_size': dp(16),
                    'color': (1, 0, 0, 1),
                    'halign': 'center',
                    'valign': 'middle',
                    'size_hint_y': None,
                    'height': dp(40)
                }
                
                # 如果有加载的字体，使用它
                if DEFAULT_FONT:
                    error_config['font_name'] = DEFAULT_FONT
                
                error_label = Label(**error_config)
                qr_window.add_widget(error_label)
                
        except Exception as e:
            error_config = {
                'text': f'图片加载错误: {str(e)}',
                'font_size': dp(14),
                'color': (1, 0, 0, 1),
                'halign': 'center',
                'valign': 'middle',
                'size_hint_y': None,
                'height': dp(40)
            }
            
            # 如果有加载的字体，使用它
            if DEFAULT_FONT:
                error_config['font_name'] = DEFAULT_FONT
            
            error_label = Label(**error_config)
            qr_window.add_widget(error_label)
        
        # 关闭按钮
        close_btn = Button(
            text='关闭',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        
        from kivy.uix.popup import Popup
        popup = Popup(
            title='二维码',
            content=qr_window,
            size_hint=(0.8, 0.8),
            auto_dismiss=False
        )
        
        close_btn.bind(on_press=popup.dismiss)
        qr_window.add_widget(close_btn)
        
        popup.open()
        self.status_label.text = '二维码已显示'
    
    def get_qr_path(self):
        """获取二维码图片路径（适配安卓路径）"""
        # 安卓打包后的路径处理
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller打包路径
            base_path = Path(sys._MEIPASS)
        else:
            # 正常Python路径
            base_path = Path(__file__).parent
        
        # 尝试多个可能的路径
        possible_paths = [
            base_path / "asset" / "qr_wechat.png",
            base_path / "assets" / "qr_wechat.png",
            base_path / "qr_wechat.png",
            Path("asset") / "qr_wechat.png",
            Path("assets") / "qr_wechat.png",
            "qr_wechat.png"
        ]
        
        print(f"当前工作目录: {os.getcwd()}")
        print(f"基础路径: {base_path}")
        
        for path in possible_paths:
            print(f"尝试路径: {path}")
            if path.exists():
                print(f"✅ 找到文件: {path}")
                return str(path)
        
        # 如果都没找到，返回默认路径
        print("⚠️ 未找到二维码文件，使用默认路径")
        return str(possible_paths[0])
    
    def show_help(self, instance):
        """显示使用说明"""
        help_text = """
使用说明：

1. 选择视频平台：点击对应平台按钮
2. 显示二维码：点击"显示二维码"按钮
3. 扫码关注公众号获取最新资源
4. 在浏览器中享受VIP视频资源

注意事项：
- 本应用仅提供平台导航功能
- 实际视频内容在各个平台官网
- 请遵守相关法律法规
        """
        
        from kivy.uix.popup import Popup
        # 创建带滚动条的内容区域
        content_layout = ScrollView(do_scroll_y=True, do_scroll_x=False)
        
        label_config = {
            'text': help_text,
            'markup': False,  # 禁用markup以避免可能的显示问题
            'font_size': dp(15),
            'color': (1, 1, 1, 1),
            'halign': 'left',
            'valign': 'top',
            'text_size': (None, None),  # 让文本自然换行
            'size_hint_y': None,
            'padding': [dp(10), dp(10)]
        }
        
        # 如果有加载的字体，使用它
        if DEFAULT_FONT:
            label_config['font_name'] = DEFAULT_FONT
        
        content_label = Label(**label_config)
        content_label.bind(texture_size=content_label.setter('size'))
        content_layout.add_widget(content_label)
        
        popup = Popup(
            title='使用说明',
            content=content_layout,
            size_hint=(0.9, 0.7)
        )
        popup.open()
        self.status_label.text = '已显示使用说明'
    
    def show_about(self, instance):
        """显示关于信息"""
        about_text = """
VIP追剧神器 v1.0.0

基于Kivy框架开发的安卓应用
提供便捷的视频平台导航服务

功能特性：
- 📱 移动端适配界面
- 🎯 多平台快速导航
- 📸 二维码扫码关注
- 🔗 网址解析播放
- 🎨 现代化UI设计

开发：VIP追剧神器团队
版本：Android 1.0.0

仅供学习参考，请于24小时内删除
        """
        from kivy.uix.popup import Popup
        # 创建带滚动条的内容区域
        content_layout = ScrollView(do_scroll_y=True, do_scroll_x=False)
        
        label_config = {
            'text': about_text,
            'markup': False,  # 禁用markup以避免可能的显示问题
            'font_size': dp(15),
            'color': (1, 1, 1, 1),
            'halign': 'left',
            'valign': 'top',
            'text_size': (None, None),  # 让文本自然换行
            'size_hint_y': None,
            'padding': [dp(10), dp(10)]
        }
        
        # 如果有加载的字体，使用它
        if DEFAULT_FONT:
            label_config['font_name'] = DEFAULT_FONT
        
        content_label = Label(**label_config)
        content_label.bind(texture_size=content_label.setter('size'))
        content_layout.add_widget(content_label)
        
        popup = Popup(
            title='关于应用',
            content=content_layout,
            size_hint=(0.8, 0.6)
        )
        popup.open()
        self.status_label.text = '已显示关于信息'
    
    def clear_url_input(self, instance):
        """清空URL输入框"""
        self.url_input.text = ''
        self.status_label.text = '已清空输入框'
    
    def play_from_url(self, instance):
        """从URL播放视频"""
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = '请输入有效的URL'
            return
        
        # 获取选中的解析接口
        selected_api = 1  # 默认
        for api_num, radio_btn in self.api_radios:
            if radio_btn.active:
                selected_api = api_num
                break
        
        # 定义不同的解析接口URL模板
        api_templates = {
            1: "https://jx.xmflv.cc/?url={}",
            2: "https://jx.m3u8.tv/jiexi/?url={}",
            3: "https://www.yemu.xyz/?url={}"
        }
        
        # 确保URL格式正确，如果没有协议，添加http://
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url
        
        # 根据选择的接口拼接最终URL
        final_url = api_templates.get(selected_api, api_templates[1]).format(url)
        
        self.status_label.text = f'正在使用接口{selected_api}解析...'
        
        # 在新线程中打开URL
        def open_url():
            try:
                print(f"打开拼接后的URL: {final_url}")
                webbrowser.open(final_url)
                self.status_label.text = f'接口{selected_api}播放成功'
            except Exception as e:
                self.status_label.text = f'播放失败: {str(e)}'
        
        threading.Thread(target=open_url, daemon=True).start()

if __name__ == '__main__':
    # 确保asset目录存在
    asset_dir = Path("asset")
    if not asset_dir.exists():
        asset_dir.mkdir()
        print(f"✅ 创建asset目录: {asset_dir}")
    
    print("🚀 启动VIP追剧神器 - Android版本")
    print("📱 应用正在初始化...")
    
    try:
        app = VipVideoApp()
        app.run()
    except Exception as e:
        print(f"❌ 应用启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)