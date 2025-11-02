"""
此代码需在 python 环境下运行, ✨你还年轻，你把钱给我，你自己再去赚可以吗？
如果你觉得这个对你有帮助，欢迎您的打赏。我会非常感激你的慷慨和鼓励(*^▽^*)
"""
import tkinter as tk
import webbrowser
from tkinter import messagebox
import re
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class VipVideoNavigation:
    def __init__(self, root):
        self.root = root
        self.root.title('VIP追剧神器')
        self.root.geometry('500x550')  # 增加窗口高度以容纳更大的二维码和文字
        self.root.resizable(False, False)  # 锁定窗口尺寸
        self.create_widgets()

    def create_widgets(self):
        # 找电影标签
        find_movie = tk.Label(self.root, text='去找电影：')
        find_movie.place(x=20, y=20, width=100, height=30)
        
        # 平台按钮
        platforms = [
            ('爱奇艺', self.open_iqy, 125),
            ('腾讯视频', self.open_tx, 225),
            ('优酷视频', self.open_yq, 325)
        ]
        for text, command, xpos in platforms:
            tk.Button(self.root, text=text, command=command)\
                .place(x=xpos, y=10, width=80, height=40)

        # 输入区域
        label_movie_link = tk.Label(self.root, text='输入网址：')
        label_movie_link.place(x=20, y=60, width=100, height=30)

        self.entry_movie_link = tk.Entry(self.root)
        self.entry_movie_link.place(x=125, y=60, width=260, height=30)
        self.entry_movie_link.bind('<Return>', lambda event: self.play_video())  # 回车播放

        button_movie_link = tk.Button(self.root, text='清空', command=self.empty)
        button_movie_link.place(x=390, y=60, width=40, height=30)   
        
        button_movie_link = tk.Button(self.root, text='播放', command=self.play_video)
        button_movie_link.place(x=435, y=60, width=40, height=30)

        # 解析接口选择
        parse_label = tk.Label(self.root, text='解析接口：')
        parse_label.place(x=20, y=100, width=100, height=30)
        
        self.parse_var = tk.StringVar()
        parse_options = [
            ("接口1", "https://jx.xmflv.cc/?url="),
            ("接口2", "https://jx.m3u8.tv/jiexi/?url="),
            ("接口3", "https://www.yemu.xyz/?url="),
        ]
        
        # 设置默认选中接口1
        self.parse_var.set("https://jx.xmflv.cc/?url=")
        
        x_offset = 125
        for i, (text, url) in enumerate(parse_options):
            radio = tk.Radiobutton(self.root, text=text, variable=self.parse_var, 
                                  value=url, command=self.select_parse)
            radio.place(x=x_offset, y=100, width=60, height=30)
            x_offset += 65
            # 如果一行放不下，可以考虑换行显示
            if x_offset > 450 and i < len(parse_options) - 1:
                x_offset = 125

        # 安全提示标签
        tip_label = tk.Label(self.root, text='请勿相信播放页面的广告，保护好自己的钱袋子。', 
                            fg='red', font=('Arial', 9))
        tip_label.place(x=20, y=140, width=460, height=30)

        # 收款二维码
        self.load_qr_code()

        # 温馨提示文字
        thank_you_label = tk.Label(self.root, text='感谢您的支持！✨', 
                                  font=('Arial', 10, 'bold'), fg='green')
        thank_you_label.place(x=180, y=550, width=140, height=20)
        
        support_label = tk.Label(self.root, text='如果觉得好用，欢迎打赏一瓶水~', 
                                font=('Arial', 9))
        support_label.place(x=130, y=550, width=240, height=20)


    def load_qr_code(self):
        """加载二维码图片"""
        try:
            if PIL_AVAILABLE:
                # 使用PIL加载图片，支持更多格式
                image = Image.open('./asset/qr_wechat.png')
                # 调整图片大小为150x150像素
                image = image.resize((250, 250))
                self.qr_code = ImageTk.PhotoImage(image)
            else:
                # 如果没有PIL，则使用原始方式（仅支持GIF/PNG）
                self.qr_code = tk.PhotoImage(file='./asset/qr_wechat.png')
            
            # 将二维码放置在窗口中央下方
            qr_label = tk.Label(self.root, image=self.qr_code)
            qr_label.place(x=125, y=200, width=250, height=250)
            # 保持引用防止被垃圾回收
            qr_label.image = self.qr_code
        except Exception as e:
            # 如果图片加载失败，显示提示文字
            qr_error_label = tk.Label(self.root, text='二维码加载失败', fg='gray')
            qr_error_label.place(x=15, y=200, width=250, height=250)
            print(f"二维码加载失败: {e}")


    def select_parse(self):
        # 选择解析接口
        pass

    def open_iqy(self):
        webbrowser.open('https://www.iqiyi.com')
        
    def open_tx(self):
        webbrowser.open('https://v.qq.com')
        
    def open_yq(self):
        webbrowser.open('https://www.youku.com/')
        
    def validate_url(self, url):
        # 简单验证URL格式
        pattern = r'^https?://'
        return re.match(pattern, url) is not None
        
    def play_video(self):
        url = self.entry_movie_link.get().strip()
        if not url:
            messagebox.showwarning("警告", "请输入视频网址！")
            return
            
        if not self.validate_url(url):
            messagebox.showwarning("警告", "请输入有效的网址！\n网址应以http://或https://开头")
            return
            
        parse_url = self.parse_var.get()
        try:
            webbrowser.open(f'{parse_url}{url}')
        except Exception as e:
            messagebox.showerror("错误", f"播放失败：{str(e)}")

    def empty(self):
        self.entry_movie_link.delete(0, tk.END)


if __name__ == '__main__':
    root = tk.Tk()
    app = VipVideoNavigation(root)
    root.mainloop()