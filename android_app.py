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
# PIL库不再需要，因为已移除二维码功能
import requests
import threading
from kivy.graphics import Color, RoundedRectangle, Rectangle, BorderImage
from kivy.uix.effectwidget import EffectWidget
from kivy.animation import Animation

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
Window.clearcolor = (0.05, 0.05, 0.08, 1)  # 更现代的深色背景
Window.fullscreen = False
Window.resizable = True

# 创建自定义圆角按钮类
class RoundedButton(Button):
    """自定义圆角按钮，带有阴影效果"""
    def __init__(self, **kwargs):
        # 从kwargs中提取圆角半径
        self.radius_val = kwargs.pop('radius', [15, 15, 15, 15])
        # 从kwargs中提取背景色
        self.bg_color = kwargs.pop('bg_color', (0.5, 0.5, 0.5, 1))
        # 设置阴影属性
        self.shadow_offset_val = kwargs.pop('shadow_offset', (2, -2))
        self.shadow_color_val = kwargs.pop('shadow_color', (0, 0, 0, 0.5))
        
        # 设置默认背景为透明
        kwargs['background_normal'] = ''
        kwargs['background_down'] = ''
        
        # 确保文本颜色设置正确
        if 'color' not in kwargs:
            kwargs['color'] = (1, 1, 1, 1)  # 默认白色文本
        
        # 确保字体设置正确
        if DEFAULT_FONT and 'font_name' not in kwargs:
            kwargs['font_name'] = DEFAULT_FONT
        
        # 初始化父类
        super(RoundedButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # 透明背景
        
        # 设置背景和阴影
        with self.canvas.before:
            # 阴影
            Color(*self.shadow_color_val)
            self.shadow = RoundedRectangle(
                pos=(self.pos[0] + self.shadow_offset_val[0], self.pos[1] + self.shadow_offset_val[1]),
                size=self.size,
                radius=self.radius_val
            )
            # 背景
            Color(*self.bg_color)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.radius_val
            )
        
        # 绑定位置和大小变化
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # 添加按下动画效果
        self.bind(state=self.on_state_change)
    
    def update_rect(self, instance, value):
        # 更新背景和阴影位置
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.shadow.pos = (self.pos[0] + self.shadow_offset_val[0], self.pos[1] + self.shadow_offset_val[1])
        self.shadow.size = self.size
    
    def on_state_change(self, instance, value):
        # 当按钮状态改变时的动画效果
        if value == 'down':
            # 按下状态
            anim = Animation(size=(self.size[0] * 0.95, self.size[1] * 0.95), duration=0.1)
            anim.start(self)
        else:
            # 释放状态
            anim = Animation(size=(self.size[0] / 0.95, self.size[1] / 0.95), duration=0.1)
            anim.start(self)

# 创建自定义卡片布局类
class CardLayout(BoxLayout):
    """自定义卡片布局，带有阴影和圆角效果"""
    def __init__(self, **kwargs):
        # 从kwargs中提取背景颜色，如果没有提供则使用默认值
        bg_color = kwargs.pop('background_color', (0.1, 0.1, 0.2, 0.8))
        # 从kwargs中提取圆角半径
        self.radius_val = kwargs.pop('radius', [12, 12, 12, 12])
        # 从kwargs中提取阴影偏移
        self.shadow_offset_val = kwargs.pop('shadow_offset', (3, -3))
        # 从kwargs中提取阴影颜色
        self.shadow_color_val = kwargs.pop('shadow_color', (0, 0, 0, 0.3))
        super(CardLayout, self).__init__(**kwargs)
        
        # 设置背景和阴影
        with self.canvas.before:
            # 阴影
            Color(*self.shadow_color_val)
            self.shadow = RoundedRectangle(
                pos=(self.pos[0] + self.shadow_offset_val[0], self.pos[1] + self.shadow_offset_val[1]),
                size=self.size,
                radius=self.radius_val
            )
            # 背景
            Color(*bg_color)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.radius_val
            )
        
        # 绑定位置和大小变化
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, instance, value):
        # 更新背景和阴影位置
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.shadow.pos = (self.pos[0] + self.shadow_offset_val[0], self.pos[1] + self.shadow_offset_val[1])
        self.shadow.size = self.size

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
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(15), size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # 标题区域
        title_card = CardLayout(orientation='vertical', padding=dp(15), size_hint_y=None, height=dp(80), background_color=(0.15, 0.15, 0.3, 0.9))
        
        # 标题 - 添加字体设置
        title_config = {
            'text': 'VIP追剧神器',
            'font_size': dp(28),
            'size_hint_y': None,
            'height': dp(60),
            'color': (1, 0.8, 0.2, 1),
            'halign': 'center',
            'valign': 'middle',
            'bold': True
        }
        
        # 如果有加载的字体，使用它
        if DEFAULT_FONT:
            title_config['font_name'] = DEFAULT_FONT
        
        title_label = Label(**title_config)
        title_card.add_widget(title_label)
        main_layout.add_widget(title_card)
        
        # 热门平台区域已移除
        
        # 搜索平台区域
        search_card = CardLayout(orientation='vertical', padding=dp(15), size_hint_y=None, height=dp(140))
        
        # 搜索标题
        search_label_config = {
            'text': '快速搜索',
            'font_size': dp(18),
            'size_hint_y': None,
            'height': dp(40),
            'color': (0.9, 0.9, 0.9, 1),
            'halign': 'left',
            'valign': 'middle',
            'bold': True
        }
        if DEFAULT_FONT:
            search_label_config['font_name'] = DEFAULT_FONT
        search_label = Label(**search_label_config)
        search_card.add_widget(search_label)
        
        # 平台快捷按钮
        quick_platforms_layout = GridLayout(
            cols=3, 
            spacing=dp(8), 
            size_hint_y=None,
            height=dp(70)
        )
        
        quick_platforms = [
            {"name": "爱奇艺", "bg_color": (0.2, 0.7, 0.3, 1)},
            {"name": "腾讯视频", "bg_color": (0.2, 0.45, 0.8, 1)},
            {"name": "优酷视频", "bg_color": (0.9, 0.25, 0.25, 1)}
        ]
        
        for platform in quick_platforms:
            quick_btn_config = {
                'text': platform["name"],
                'bg_color': platform["bg_color"],
                'color': (1, 1, 1, 1),  # 设置文本颜色为白色
                'font_size': dp(14),
                'size_hint_y': None,
                'height': dp(60),
                'halign': 'center',
                'valign': 'middle',
                'radius': [12, 12, 12, 12]  # 更小的圆角
            }
            
            if DEFAULT_FONT:
                quick_btn_config['font_name'] = DEFAULT_FONT
            
            btn = RoundedButton(**quick_btn_config)
            btn.bind(on_press=self.on_platform_click)
            quick_platforms_layout.add_widget(btn)
        
        search_card.add_widget(quick_platforms_layout)
        main_layout.add_widget(search_card)
        
        # 网址输入区域
        url_card = CardLayout(orientation='vertical', padding=dp(15), size_hint_y=None, height=dp(170))
        
        # 网址输入标题
        url_label_config = {
            'text': '视频解析',
            'font_size': dp(18),
            'size_hint_y': None,
            'height': dp(40),
            'color': (0.9, 0.9, 0.9, 1),
            'halign': 'left',
            'valign': 'middle',
            'bold': True
        }
        if DEFAULT_FONT:
            url_label_config['font_name'] = DEFAULT_FONT
        url_label = Label(**url_label_config)
        url_card.add_widget(url_label)
        
        # 输入框（带圆角效果）
        from kivy.uix.textinput import TextInput
        self.url_input = TextInput(
            text='',
            multiline=False,
            font_size=dp(14),
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.2, 0.3, 1),
            foreground_color=(1, 1, 1, 1),
            padding=[dp(10), dp(10)]
        )
        if DEFAULT_FONT:
            self.url_input.font_name = DEFAULT_FONT
        
        # 为输入框添加圆角
        with self.url_input.canvas.before:
            Color(0.2, 0.2, 0.3, 1)
            RoundedRectangle(pos=self.url_input.pos, size=self.url_input.size, radius=[10, 10, 10, 10])
        self.url_input.bind(pos=lambda *args: self.update_input_rect(self.url_input), 
                          size=lambda *args: self.update_input_rect(self.url_input))
        
        url_card.add_widget(self.url_input)
        
        # 按钮布局
        url_buttons_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        
        clear_btn = RoundedButton(
            text='清空',
            bg_color=(0.25, 0.1, 0.1, 0.9),
            color=(1, 1, 1, 1),  # 设置文本颜色为白色
            font_size=dp(16),
            size_hint_x=0.5,
            halign='center',
            valign='middle'
        )
        if DEFAULT_FONT:
            clear_btn.font_name = DEFAULT_FONT
        clear_btn.bind(on_press=self.clear_url_input)
        
        play_btn = RoundedButton(
            text='播放',
            bg_color=(0.1, 0.5, 0.2, 0.9),
            color=(1, 1, 1, 1),  # 设置文本颜色为白色
            font_size=dp(16),
            size_hint_x=0.5,
            halign='center',
            valign='middle'
        )
        if DEFAULT_FONT:
            play_btn.font_name = DEFAULT_FONT
        play_btn.bind(on_press=self.play_from_url)
        
        url_buttons_layout.add_widget(clear_btn)
        url_buttons_layout.add_widget(play_btn)
        url_card.add_widget(url_buttons_layout)
        
        main_layout.add_widget(url_card)
        
        # 解析接口选择区域
        api_card = CardLayout(orientation='vertical', padding=dp(15), size_hint_y=None, height=dp(120))
        
        # 接口选择标题
        api_label_config = {
            'text': '解析接口',
            'font_size': dp(18),
            'size_hint_y': None,
            'height': dp(40),
            'color': (0.9, 0.9, 0.9, 1),
            'halign': 'left',
            'valign': 'middle',
            'bold': True
        }
        if DEFAULT_FONT:
            api_label_config['font_name'] = DEFAULT_FONT
        api_label = Label(**api_label_config)
        api_card.add_widget(api_label)
        
        # 接口选择布局
        self.api_group = BoxLayout(orientation='horizontal', spacing=dp(25), size_hint_y=None, height=dp(50))
        
        from kivy.uix.checkbox import CheckBox
        
        # 自定义CheckBox样式
        class StyledCheckBox(CheckBox):
            def __init__(self, **kwargs):
                super(StyledCheckBox, self).__init__(**kwargs)
                self.size_hint = (None, None)
                self.size = (dp(25), dp(25))
                self.color = (0.4, 0.6, 1, 1)
        
        # 存储单选按钮引用
        self.api_radios = []
        
        for i in range(1, 4):
            api_item_layout = BoxLayout(orientation='horizontal', spacing=dp(8), size_hint=(None, 1))
            
            # 使用自定义CheckBox
            check_box = StyledCheckBox(group='api')
            if i == 1:  # 默认选择第一个
                check_box.active = True
            
            # 保存引用以便后续获取选中项
            self.api_radios.append((i, check_box))
            
            radio_label_config = {
                'text': f'接口{i}',
                'font_size': dp(16),
                'color': (0.9, 0.9, 0.9, 1),
                'valign': 'middle'
            }
            if DEFAULT_FONT:
                radio_label_config['font_name'] = DEFAULT_FONT
            radio_label = Label(**radio_label_config)
            
            api_item_layout.add_widget(check_box)
            api_item_layout.add_widget(radio_label)
            self.api_group.add_widget(api_item_layout)
        
        api_card.add_widget(self.api_group)
        main_layout.add_widget(api_card)
        
        # 警告信息卡片
        warning_card = CardLayout(orientation='vertical', padding=dp(15), size_hint_y=None, height=dp(80), background_color=(0.25, 0.1, 0.1, 0.9))
        
        warning_label_config = {
            'text': '⚠️ 请勿相信播放页面的广告，保护好自己的钱袋子。',
            'font_size': dp(15),
            'size_hint_y': None,
            'height': dp(50),
            'color': (1, 0.3, 0.3, 1),
            'halign': 'center',
            'valign': 'middle',
            'text_size': (dp(300), None)
        }
        if DEFAULT_FONT:
            warning_label_config['font_name'] = DEFAULT_FONT
        warning_label = Label(**warning_label_config)
        warning_card.add_widget(warning_label)
        main_layout.add_widget(warning_card)
        
        # 功能按钮区域
        functions_card = CardLayout(orientation='vertical', padding=dp(15), size_hint_y=None, height=dp(160))
        
        # 创建功能按钮的通用函数
        def create_function_button(text, color):
            btn_config = {
                'text': text,
                'color': color,
                'font_size': dp(16),
                'size_hint_y': None,
                'height': dp(60),
                'halign': 'center',
                'valign': 'middle',
                'radius': [15, 15, 15, 15]
            }
            
            # 如果有加载的字体，使用它
            if DEFAULT_FONT:
                btn_config['font_name'] = DEFAULT_FONT
            
            return RoundedButton(**btn_config)
        
        # 功能按钮区域已移除
        
        # 状态标签卡片
        status_card = CardLayout(orientation='vertical', padding=dp(15), size_hint_y=None, height=dp(80), background_color=(0.1, 0.2, 0.3, 0.9))
        
        status_config = {
            'text': '欢迎使用VIP追剧神器',
            'font_size': dp(15),
            'size_hint_y': None,
            'height': dp(50),
            'color': (0.8, 0.9, 1, 1),
            'halign': 'center',
            'valign': 'middle',
            'text_size': (dp(300), None)
        }
        
        # 如果有加载的字体，使用它
        if DEFAULT_FONT:
            status_config['font_name'] = DEFAULT_FONT
        
        self.status_label = Label(**status_config)
        status_card.add_widget(self.status_label)
        main_layout.add_widget(status_card)
        
        # 将主布局添加到ScrollView中
        root_layout.add_widget(main_layout)
        
        return root_layout
    
    def update_input_rect(self, widget):
        """更新输入框的背景矩形位置和大小"""
        if hasattr(widget, 'input_rect'):
            widget.input_rect.pos = widget.pos
            widget.input_rect.size = widget.size
    
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
                "优酷": "https://www.youku.com"
            }
            
            url = platforms.get(platform_name, "https://www.youku.com")
            try:
                webbrowser.open(url)
                self.status_label.text = f'已打开 {platform_name}'
            except Exception as e:
                self.status_label.text = f'打开失败: {str(e)}'
        
        # 在新线程中打开，避免阻塞UI
        threading.Thread(target=open_platform, daemon=True).start()
    

    
    def show_help(self, instance):
        """显示使用说明弹窗"""
        from kivy.uix.modalview import ModalView
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.scrollview import ScrollView
        
        # 创建自定义弹窗
        popup = ModalView(size_hint=(0.85, 0.9), background_color=(0, 0, 0, 0.9), auto_dismiss=False)
        
        # 主布局
        layout = CardLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # 标题
        title_config = {
            'text': '使用说明',
            'font_size': dp(22),
            'color': (0.9, 0.9, 0.9, 1),
            'halign': 'center',
            'valign': 'middle',
            'size_hint_y': None,
            'height': dp(60),
            'bold': True
        }
        if DEFAULT_FONT:
            title_config['font_name'] = DEFAULT_FONT
        title_label = Label(**title_config)
        layout.add_widget(title_label)
        
        # 创建ScrollView
        scroll_view = ScrollView(size_hint=(1, 1))
        
        # 内容容器
        content_container = BoxLayout(orientation='vertical', padding=dp(10))
        
        # 内容标签
        content_config = {
            'text': (
                '1. 快速搜索功能：\n'
                '   - 点击对应的平台按钮，快速跳转到相应的视频平台。\n'
                '\n'
                '2. 视频解析功能：\n'
                '   - 在输入框中粘贴视频链接。\n'
                '   - 选择一个解析接口。\n'
                '   - 点击播放按钮进行解析观看。\n'
                '\n'
                '3. 注意事项：\n'
                '   - 请确保输入的链接正确无误。\n'
                '   - 如果一个接口无法解析，可以尝试更换其他接口。\n'
                '   - 请勿相信播放页面上的广告。\n'
                '   - 本应用仅提供视频解析服务，所有内容版权归原平台所有。'
            ),
            'font_size': dp(16),
            'color': (0.9, 0.9, 0.9, 1),
            'halign': 'left',
            'valign': 'top',
            'text_size': (dp(320), None)
        }
        if DEFAULT_FONT:
            content_config['font_name'] = DEFAULT_FONT
        content_label = Label(**content_config)
        content_container.add_widget(content_label)
        
        scroll_view.add_widget(content_container)
        layout.add_widget(scroll_view)
        
        # 关闭按钮
        close_btn = RoundedButton(
            text='关闭',
            size_hint_y=None,
            height=dp(60),
            color=(0.9, 0.3, 0.3, 1),
            font_size=dp(18),
            radius=[15, 15, 15, 15]
        )
        if DEFAULT_FONT:
            close_btn.font_name = DEFAULT_FONT
        close_btn.bind(on_press=popup.dismiss)
        layout.add_widget(close_btn)
        
        # 添加布局到弹窗
        popup.add_widget(layout)
        popup.open()
        self.status_label.text = '已显示使用说明'
    

    
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