import os
import sys
import tkinter as tk
import tkinter.font as tkFont

from PIL import Image, ImageTk

_VERSION_ = "1.0.0"


def resource_path(relative_path):
    """获得资源的绝对路径，无论是开发环境还是打包后一文件模式。"""
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后，资源会被解压到 _MEIPASS
        base = sys._MEIPASS
    else:
        # 开发环境下
        base = os.path.abspath(".")
    return os.path.join(base, relative_path)


class MapTool(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title(f"Valorant Map Tool v{_VERSION_}")
        self.geometry("1200x1020")
        self.resizable(False, False)
        self.iconbitmap(resource_path("KO.ico"))
        
        # 定义一个字体变量
        self.ctrl_font = tkFont.Font(family="Microsoft Yahei", size=12)

        # 资源路径设置
        self.maps_dir = resource_path("maps")
        self.ref_path = resource_path("reference_line.png")
        
        # 获取地图列表
        self.map_files = sorted(
            f for f in os.listdir(self.maps_dir)
            if f.lower().endswith(".png")
        )
        
        # 缓存：只存 PhotoImage，不存 PIL.Image
        self.map_images = {}

        # 预加载第一张地图，和参考线
        first_map = self.map_files[0]
        self.map_images[first_map] = ImageTk.PhotoImage(
            Image.open(os.path.join(self.maps_dir, first_map))
        )
        self.ref_image = ImageTk.PhotoImage(
            Image.open(self.ref_path)
        )
        
        # 控制变量
        self.var_show_ref = tk.BooleanVar(value=True)
        self.var_map = tk.StringVar(value=first_map)
        
        # 左侧面板
        control = tk.Frame(self)
        control.pack(side="left", fill="y", padx=10, pady=10)

        # 1. 显示参考线 复选框（最上面）
        cb = tk.Checkbutton(
            control, text="显示参考线",
            font=self.ctrl_font,
            variable=self.var_show_ref,
            command=self._on_ref_toggle
        )
        cb.pack(anchor="w", pady=(0, 15))

        # 2. 地图单选框
        tk.Label(control, text="选择地图：", font=self.ctrl_font).pack(anchor="w")
        for fn in self.map_files:
            name = os.path.splitext(fn)[0]
            rb = tk.Radiobutton(
                control, text=name,
                font=self.ctrl_font,
                variable=self.var_map, value=fn,
                command=self._on_map_change
            )
            rb.pack(anchor="w")

        # 右侧画布
        self.canvas = tk.Canvas(
            self, width=1000, height=1000,
            bg="white"
        )
        self.canvas.pack(side="right", padx=10, pady=10)
        
        # 绑定单击事件：点击任意点都能定位参考线
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        
        # 初始化：画上第一张地图 & 参考线
        self._draw_map()
        self._draw_ref()
    
    def _draw_map(self):
        self.canvas.delete("map")
        fn = self.var_map.get()
        # 按需加载：如果没缓存再打开并转换
        if fn not in self.map_images:
            path = os.path.join(self.maps_dir, fn)
            img = Image.open(path)
            self.map_images[fn] = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0,
                                 image=self.map_images[fn],
                                 anchor="nw", tag="map")
    
    def _draw_ref(self):
        if self.var_show_ref.get():
            # 如果尚未创建，就在中心创建
            if not self.canvas.find_withtag("ref"):
                self.canvas.create_image(
                    500, 500, image=self.ref_image,
                    anchor="center", tag="ref"
                )
                # 参考线可拖拽
                self.canvas.tag_bind("ref", "<B1-Motion>",
                                     self._on_drag_ref)
            else:
                # 已创建则显示
                self.canvas.itemconfigure("ref", state="normal")
            # 确保在最顶层
            self.canvas.tag_raise("ref")
        else:
            self.canvas.itemconfigure("ref", state="hidden")
    
    def _on_map_change(self):
        self._draw_map()
        if self.var_show_ref.get():
            self.canvas.tag_raise("ref")
    
    def _on_ref_toggle(self):
        self._draw_ref()
    
    def _on_drag_ref(self, event):
        self.canvas.coords("ref", event.x, event.y)
    
    def _on_canvas_click(self, event):
        # 只有在显示参考线时生效
        if self.var_show_ref.get() and self.canvas.find_withtag("ref"):
            self.canvas.coords("ref", event.x, event.y)


if __name__ == "__main__":
    app = MapTool()
    app.mainloop()
