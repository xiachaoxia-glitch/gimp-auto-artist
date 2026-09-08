# GIMP Auto Artist 🎨✨

> **Python & GIMP Script-Fu Toolkit for Automated Poster, Banner, and Graphic Design**
> 基于 Python 与 GIMP Script-Fu / Pillow 的自动化海报排版、矢量几何绘画与图形设计工具链。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)]()
[![GIMP: Compatible](https://img.shields.io/badge/GIMP-Python--Fu%20%26%20Script--Fu-purple.svg)]()

---

## 🌟 核心功能 (Features)

- 🖼️ **自动化海报生成 (`create_poster.py`)**：根据配置自动渲染背景渐变、多行标题文字对齐排版、阴影与装帧装饰线条。
- 🌄 **风景艺术生成器 (`generators/landscape_painting.py`)**：纯程序化渐变渲染日落天空、山峦起伏多边形、湖泊倒影与落日余晖。
- 👤 **人物肖像生成器 (`generators/character_portrait.py`)**：参数化高精度五官、发丝散落与层次腮红混色。
- 🔌 **GIMP Script-Fu 自动化集成**：支持通过 GIMP 命令行以 Batch 模式静默调用脚本，实现无头（Headless）批处理。

---

## 🚀 快速上手 (Quick Start)

### 1. 安装依赖

```bash
git clone https://github.com/xiachaoxia-glitch/gimp-auto-artist.git
cd gimp-auto-artist

pip install -r requirements.txt
```

### 2. 生成示例画作与海报

```bash
# 生成商业/活动宣传海报
python create_poster.py

# 程序化生成山间日落风景画
python generators/landscape_painting.py

# 生成精细人像插画
python generators/character_portrait.py
```
*所有生成的图片将自动保存至 `./output/` 目录下。*

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。
