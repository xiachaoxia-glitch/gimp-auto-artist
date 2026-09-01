#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高质感现代企业招聘海报自动化生成脚本 (Pillow 矢量与渐变渲染)
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 800, 1200

# ===== 调色板 =====
C = {
    'bg_top': (15, 20, 60),
    'bg_bottom': (25, 55, 109),
    'accent1': (255, 65, 54),     # 亮红
    'accent2': (0, 180, 255),     # 亮蓝
    'accent3': (255, 190, 50),    # 暖金
    'accent4': (46, 213, 115),    # 翠绿
    'accent5': (200, 80, 192),    # 紫色
    'white': (255, 255, 255),
    'off_white': (240, 245, 255),
    'soft_blue': (180, 210, 255),
    'dark_text': (20, 30, 60),
    'gold': (255, 215, 0),
}


def load_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


fonts = {
    'company': load_font(28, bold=True),
    'sub_en': load_font(16),
    'title': load_font(72, bold=True),
    'slogan': load_font(32, bold=True),
    'pos_name': load_font(24),
    'pos_count': load_font(24, bold=True),
    'body': load_font(20),
    'contact_label': load_font(20, bold=True),
    'contact_val': load_font(20),
    'small': load_font(16),
    'tiny': load_font(14),
}


def tw(d, text, font):
    b = d.textbbox((0, 0), text, font=font)
    return b[2] - b[0]


def center_text(d, text, font, y, fill):
    x = (W - tw(d, text, font)) // 2
    d.text((x, y), text, fill=fill, font=font)


def draw_gradient(d, y1, y2, c1, c2):
    """垂直渐变条"""
    h = max(1, y2 - y1)
    for i in range(h):
        r = int(c1[0] + (c2[0] - c1[0]) * i / h)
        g = int(c1[1] + (c2[1] - c1[1]) * i / h)
        b = int(c1[2] + (c2[2] - c1[2]) * i / h)
        d.line([(0, y1 + i), (W, y1 + i)], fill=(r, g, b))


def generate_poster(output_path="output/recruitment_poster.png"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img = Image.new('RGB', (W, H), C['bg_top'])
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, 0, H, C['bg_bottom'], C['bg_top'])

    # 散落光点
    random.seed(42)
    for _ in range(150):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.choice([1, 2, 3])
        draw.ellipse([(x, y), (x + s, y + s)], fill=(255, 255, 255))

    # 装饰色块
    draw_gradient(draw, 0, 250, C['accent2'], C['bg_top'])
    draw.rectangle([(0, 245), (W, 250)], fill=C['accent2'])

    company = "未来创新科技有限公司"
    center_text(draw, company, fonts['company'], 50, C['gold'])
    center_text(draw, "JOIN US · 探索无限可能", fonts['sub_en'], 95, C['soft_blue'])

    # 主标题区域
    draw_gradient(draw, 260, 380, C['accent1'], (180, 30, 20))
    draw.rounded_rectangle([(30, 260), (W - 30, 380)], radius=20, outline=C['gold'], width=3)
    center_text(draw, "诚聘英才", fonts['title'], 272, C['white'])
    center_text(draw, "✦  WE WANT YOU  ✦", fonts['sub_en'], 350, C['gold'])

    # 标语
    center_text(draw, "「 寻找发光的你，与优秀同行 」", fonts['slogan'], 420, C['accent3'])

    # 职位卡片
    positions = [
        ("AI 算法与研发工程师", "2名", C['accent2']),
        ("全栈开发工程师", "3名", C['accent4']),
        ("高级产品经理", "1名", C['accent5']),
        ("商业运营主管", "2名", C['accent1']),
    ]

    card_y = 500
    card_h = 65
    card_gap = 12
    card_left = 160
    card_right = W - 80

    for i, (pos_name, count, color) in enumerate(positions):
        y = card_y + i * (card_h + card_gap)
        draw.rounded_rectangle([(card_left, y), (card_right, y + card_h)], radius=10, fill=(35, 45, 80))
        draw.rounded_rectangle([(card_left, y), (card_left + 8, y + card_h)], radius=4, fill=color)

        cx = card_left + 35
        r = 16
        draw.ellipse([(cx - r, y + card_h // 2 - r), (cx + r, y + card_h // 2 + r)], fill=color, outline=C['white'], width=2)
        center_text(draw, str(i + 1), load_font(16, bold=True), y + card_h // 2 - 11, C['white'])

        draw.text((card_left + 70, y + 15), pos_name, fill=C['white'], font=fonts['pos_name'])
        tag_x = card_right - 80
        draw.rounded_rectangle([(tag_x, y + 12), (card_right - 10, y + card_h - 12)], radius=6, fill=color)
        draw.text((tag_x + 10, y + 15), count, fill=C['white'], font=fonts['pos_count'])

    # 联系方式
    y_contact = card_y + 4 * (card_h + card_gap) + 40
    center_text(draw, "— 投递与联系 —", fonts['sub_en'], y_contact, C['gold'])

    contact_bg_top = y_contact + 35
    contact_bg_h = 130
    draw.rounded_rectangle([(120, contact_bg_top), (W - 120, contact_bg_top + contact_bg_h)], radius=15, fill=(30, 40, 75), outline=C['accent2'], width=1)

    contacts = [
        ("👤 招聘负责人", "HR 团队"),
        ("📞 联系电话", "400-000-0000 / 010-88888888"),
        ("📧 投递邮箱", "jobs@example.com"),
    ]
    for i, (label, val) in enumerate(contacts):
        cy = contact_bg_top + 15 + i * 36
        draw.text((150, cy), label, fill=C['accent3'], font=fonts['contact_label'])
        draw.text((360, cy), val, fill=C['off_white'], font=fonts['contact_val'])

    img.save(output_path, "PNG")
    print(f"Poster generated successfully: {output_path}")


if __name__ == "__main__":
    generate_poster()
