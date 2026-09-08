#!/usr/bin/env python3
"""
GIMP 写实风格美女肖像 - 更精细的绘制
使用 GIMP 的 Python-Fu
"""
from PIL import Image, ImageDraw, ImageFilter
import math, random, os

W, H = 800, 1000
img = Image.new('RGB', (W, H), (240, 225, 210))
draw = ImageDraw.Draw(img)

# ── 背景渐变 ──
for y in range(H):
    t = y / H
    r = int(245 - 40 * t)
    g = int(230 - 30 * t)
    b = int(215 - 25 * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# ── 人物居中坐标 ──
cx, cy = W//2, H//2 - 60

# ── 头发 ──
hair_base = (25, 18, 14)
# 大块头发区域
draw.ellipse([cx-200, cy-130, cx+200, cy+400], fill=hair_base)
# 头顶
draw.ellipse([cx-180, cy-160, cx+180, cy+20], fill=hair_base)
# 刘海
draw.ellipse([cx-150, cy-140, cx+150, cy+60], fill=(30, 22, 18))

# 头发丝 (使用多条弧线)
for i in range(200):
    angle = random.uniform(0.6, 2.8)
    length = random.randint(120, 350)
    x_start = cx + int(random.randint(-180, 180) * random.random())
    y_start = cy - 130 + random.randint(-20, 30)
    x_end = x_start + int(length * 0.3 * (1 if i%3==0 else -1 if i%5==0 else 0.5))
    y_end = y_start + length
    shade = random.randint(-8, 8)
    c = tuple(max(0, min(255, hair_base[j] + shade + random.randint(-3, 3))) for j in range(3))
    w = random.randint(1, 3)
    draw.line([(x_start, y_start), (x_end, y_end)], fill=c, width=w)

# 高光发丝
for _ in range(40):
    x = cx + random.randint(-120, 120)
    ys = cy - 100 + random.randint(-10, 10)
    ye = ys + random.randint(80, 200)
    draw.line([(x, ys), (x + random.randint(-10, 10), ye)], fill=(65, 52, 42), width=1)

# ── 脸部（椭圆基础 + 多边形精修） ──
# 基础脸型 - 鹅蛋脸
draw.ellipse([cx-145, cy-175, cx+145, cy+200], fill=(245, 218, 198))
# 下巴
draw.ellipse([cx-65, cy+130, cx+65, cy+220], fill=(245, 218, 198))
# 额头高光
draw.ellipse([cx-70, cy-200, cx+70, cy-120], fill=(252, 230, 212))
# 脸颊偏暗
for side in [-1, 1]:
    draw.ellipse([cx + side*130 - 30, cy-40, cx + side*130 + 30, cy+70], fill=(230, 200, 182))
# 鼻侧阴影
draw.rectangle([cx-15, cy-70, cx-5, cy+5], fill=(225, 195, 178))
draw.rectangle([cx+5, cy-70, cx+15, cy+5], fill=(225, 195, 178))
# 鼻梁高光
draw.rectangle([cx-5, cy-65, cx+5, cy+5], fill=(255, 235, 218))

# ── 眼睛 ──
def draw_eye(draw, ex, ey, is_left=True):
    # 眼白
    draw.ellipse([ex-25, ey-12, ex+25, ey+12], fill=(255, 253, 248))
    # 上眼线
    draw.arc([ex-27, ey-14, ex+27, ey+8], 180, 360, fill=(15, 10, 8), width=3)
    # 下眼线（浅）
    draw.arc([ex-25, ey-8, ex+25, ey+12], 0, 180, fill=(80, 65, 55), width=1)
    # 虹膜
    draw.ellipse([ex-14, ey-14, ex+14, ey+14], fill=(60, 45, 25))
    # 瞳孔
    draw.ellipse([ex-7, ey-7, ex+7, ey+7], fill=(10, 8, 5))
    # 虹膜纹理（辐射状线）
    for a in range(0, 360, 15):
        rad = math.radians(a)
        r1, r2 = 8, 13
        x1 = ex + int(r1 * math.cos(rad))
        y1 = ey + int(r1 * math.sin(rad))
        x2 = ex + int(r2 * math.cos(rad))
        y2 = ey + int(r2 * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=(45, 35, 20), width=1)
    # 高光
    if is_left:
        draw.ellipse([ex+2, ey-8, ex+8, ey-2], fill=(255, 255, 255))
        draw.ellipse([ex-8, ey+2, ex-4, ey+6], fill=(255, 255, 255, 150))
    else:
        draw.ellipse([ex-8, ey-8, ex-2, ey-2], fill=(255, 255, 255))
        draw.ellipse([ex+4, ey+2, ex+8, ey+6], fill=(255, 255, 255, 150))
    # 睫毛
    for _ in range(10):
        lx = ex + random.randint(-20, 20)
        ly = ey - 12 + random.randint(-2, 2)
        dx = random.randint(-4, 4)
        dy = random.randint(-8, -3)
        draw.line([(lx, ly), (lx+dx, ly+dy)], fill=(10, 8, 5), width=1)

draw_eye(draw, cx-55, cy-40, True)
draw_eye(draw, cx+55, cy-40, False)

# 双眼皮
draw.arc([cx-80, cy-62, cx-30, cy-40], 180, 360, fill=(180, 160, 148), width=1)
draw.arc([cx+30, cy-62, cx+80, cy-40], 180, 360, fill=(180, 160, 148), width=1)

# 卧蚕
draw.arc([cx-75, cy-28, cx-35, cy-18], 0, 180, fill=(210, 190, 175), width=1)
draw.arc([cx+35, cy-28, cx+75, cy-18], 0, 180, fill=(210, 190, 175), width=1)

# ── 眉毛 ──
brow = (30, 22, 18)
draw.arc([cx-90, cy-100, cx-25, cy-72], 200, 340, fill=brow, width=5)
draw.arc([cx+25, cy-100, cx+90, cy-72], 200, 340, fill=brow, width=5)
# 眉笔纹理
for _ in range(15):
    bx = cx + random.choice([-1, 1]) * (20 + random.randint(0, 50))
    by = cy - 85 + random.randint(-8, 8)
    draw.line([(bx, by), (bx + random.randint(-3, 3), by - random.randint(1, 4))], 
              fill=brow, width=1)

# ── 鼻子 ──
# 鼻梁
draw.line([(cx-3, cy-65), (cx-4, cy-5)], fill=(195, 172, 158), width=2)
draw.line([(cx+3, cy-65), (cx+4, cy-5)], fill=(205, 182, 168), width=2)
# 鼻翼
draw.ellipse([cx-22, cy-8, cx-5, cy+10], fill=(210, 185, 170))
draw.ellipse([cx+5, cy-8, cx+22, cy+10], fill=(210, 185, 170))
# 鼻头
draw.ellipse([cx-10, cy-5, cx+10, cy+8], fill=(232, 210, 195))
# 鼻头高光
draw.ellipse([cx-3, cy-1, cx+3, cy+4], fill=(250, 230, 215))

# ── 嘴巴 ──
# 上唇
draw.ellipse([cx-50, cy+20, cx+50, cy+45], fill=(200, 130, 115))
# 唇峰
draw.polygon([(cx-6, cy+20), (cx, cy+15), (cx+6, cy+20)], fill=(200, 130, 115))
# 下唇
draw.ellipse([cx-48, cy+30, cx+48, cy+65], fill=(215, 145, 130))
# 唇线
draw.arc([cx-50, cy+18, cx+50, cy+48], 180, 360, fill=(175, 105, 92), width=2)
# 下唇高光
draw.ellipse([cx-18, cy+42, cx+18, cy+55], fill=(235, 170, 155))
# 嘴角
draw.arc([cx-55, cy+22, cx-45, cy+35], 270, 360, fill=(170, 100, 88), width=2)
draw.arc([cx+45, cy+22, cx+55, cy+35], 180, 270, fill=(170, 100, 88), width=2)

# ── 耳朵 ──
for side in [-1, 1]:
    ex = cx + side * 155
    draw.ellipse([ex-25, cy-25, ex+25, cy+35], fill=(235, 205, 188))
    draw.ellipse([ex-18, cy-18, ex+18, cy+28], fill=(225, 195, 178))

# ── 下巴阴影 ──
draw.arc([cx-55, cy+95, cx+55, cy+185], 0, 180, fill=(220, 192, 175), width=2)

# ── 脖子 ──
draw.rectangle([cx-50, cy+195, cx+50, cy+280], fill=(230, 200, 182))
draw.rectangle([cx-45, cy+195, cx+45, cy+280], fill=(245, 218, 198))
# 颈部阴影
draw.line([(cx-35, cy+200), (cx-30, cy+270)], fill=(215, 188, 170), width=3)
draw.line([(cx+35, cy+200), (cx+30, cy+270)], fill=(215, 188, 170), width=3)

# ── 身体和衣服 ──
# 肩膀
for side in [-1, 1]:
    sx = cx + side * 220
    draw.ellipse([sx-80, cy+240, sx+80, cy+400], fill=(235, 205, 188))
# 上衣 - 白色衬衫
shirt = (248, 245, 240)
shirt_shadow = (228, 225, 220)
draw.polygon([
    (cx-280, cy+290), (cx-90, cy+245), (cx+90, cy+245),
    (cx+280, cy+290), (cx+260, cy+H), (cx-260, cy+H)
], fill=shirt)
# 衣领
draw.polygon([
    (cx-90, cy+245), (cx+90, cy+245),
    (cx+45, cy+305), (cx-45, cy+305)
], fill=shirt_shadow)
# 领口线
draw.line([(cx-90, cy+245), (cx-45, cy+305)], fill=(200, 195, 190), width=3)
draw.line([(cx+90, cy+245), (cx+45, cy+305)], fill=(200, 195, 190), width=3)
# 衣褶
for x in range(-200, 201, 40):
    if abs(x) < 60: continue
    draw.line([(cx+x, cy+310), (cx+x+random.randint(-8,8), cy+380)], 
              fill=shirt_shadow, width=2)
# 锁骨
draw.arc([cx-55, cy+250, cx+55, cy+285], 180, 360, fill=(210, 200, 195), width=2)

# ── 腮红 ──
blush = Image.new('RGBA', (W, H), (0, 0, 0, 0))
bdraw = ImageDraw.Draw(blush)
bdraw.ellipse([cx-110, cy+5, cx-50, cy+60], fill=(235, 155, 140, 30))
bdraw.ellipse([cx+50, cy+5, cx+110, cy+60], fill=(235, 155, 140, 30))
bdraw.ellipse([cx-8, cy-8, cx+8, cy+8], fill=(240, 185, 170, 25))
img = Image.alpha_composite(img.convert('RGBA'), blush).convert('RGB')

# ── 微柔化（保留细节） ──
img_soft = img.filter(ImageFilter.GaussianBlur(radius=0.8))
img = Image.blend(img, img_soft, 0.25)

# ── 保存 ──
out_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'portrait_v2.png')
img.save(out_path)
print(f"[OK] 已保存: {out_path}")
print(f"[INFO] 尺寸: {img.size[0]}x{img.size[1]}")
