# Valorant Map Tool

--- 

- 一个基于 Python 的 Valorant 地图投掷辅助工具
- 支持所有游戏地图
- 支持拖拽／点击定位参考线
- 资源与方法均源自 B 站 UP 主 [仇问号](https://space.bilibili.com/455537049)
- [原版工具使用教学](https://www.bilibili.com/video/BV1k8oJYVEe1)
- 开发者仅为爱好者，通过与AI交互完成了这个项目，欢迎各位指正

--- 

## ✨ 前提

1. 你需要了解挂饰描点法
2. 你需要了解参考线的作用
3. 建议观看 B 站 UP 主 [仇问号](https://space.bilibili.com/455537049) 所有关于此类内容的视频

## 🚀 快速开始

1. 安装PIL（建议使用Python 3.7+）  
   ```bash
   pip install pillow

2. 运行 main.py


## 🏗️ 打包为 exe 可执行文件

1. 安装pyinstaller
   ```bash
   pip install pyinstaller

2. 在命令行执行命令
   ```bash
   pyinstaller --onefile --windowed --icon=KO.ico --add-data "maps;maps" --add-data "reference_line.png;." --add-data "KO.ico;." --name ValorantMapTool main.py
   
3. 在 dist 文件夹中找到 exe 文件，双击运行即可。


## 📜 许可协议

- 本项目基于 MIT License 开源，详见 LICENSE 文件。


## 🙏 致谢

- 感谢 B 站 UP 主 仇问号 的原创教学
- 感谢 Python, Tkinter, Pillow 社区
- 感谢 AI 助手的陪伴与支持