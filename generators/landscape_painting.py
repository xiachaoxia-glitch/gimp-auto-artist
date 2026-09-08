#!/usr/bin/env python3
"""
山间日落 - A landscape painting using Pillow
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, random

W, H = 1200, 800

img = Image.new('RGB', (W, H))
draw = ImageDraw.Draw(img)

# ── Sky gradient (sunset) ──
for y in range(H):
    t = y / H  # 0 top, 1 bottom
    if t < 0.4:
        r = int(30 + 50 * (t / 0.4))
        g = int(20 + 40 * (t / 0.4))
        b = int(120 + 80 * (1 - t / 0.4))
    elif t < 0.7:
        s = (t - 0.4) / 0.3
        r = int(80 + 150 * s)
        g = int(60 + 120 * s)
        b = int(200 - 180 * s)
    else:
        s = (t - 0.7) / 0.3
        r = int(230 + 25 * (1 - s))
        g = int(180 - 50 * (1 - s))
        b = int(20 + 30 * (1 - s))
    draw.line([(0, y), (W, y)], fill=(min(r,255), min(g,255), min(b,255)))

# ── Sun ──
sun_x, sun_y = W // 2, int(H * 0.65)
sun_r = 70
for r in range(sun_r, 0, -1):
    t = r / sun_r
    color = (255, int(220 - 80 * t), int(50 + 100 * (1 - t)))
    draw.ellipse([sun_x - r, sun_y - r, sun_x + r, sun_y + r], fill=color)

# ── Sun glow ──
for i in range(4):
    glow_r = sun_r + 40 + i * 25
    alpha = int(50 - i * 12)
    if alpha <= 0:
        break
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([sun_x - glow_r, sun_y - glow_r, sun_x + glow_r, sun_y + glow_r],
                  fill=(255, 200, 50, alpha))
    img = Image.alpha_composite(img.convert('RGBA'), glow).convert('RGB')
    draw = ImageDraw.Draw(img)

# ── Mountains ──
def draw_mountains(draw, y_base, color, peaks, roughness=80):
    pts = [(0, y_base)]
    x = 0
    while x <= W:
        h = sum(amp * math.sin((x + phase) * freq) for amp, phase, freq in peaks)
        h = int(h * roughness)
        pts.append((x, y_base - max(0, h)))
        x += 4
    pts.append((W, y_base))
    draw.polygon(pts, fill=color)

# Far mountains (purple-blue)
draw_mountains(draw, int(H * 0.55),
    (80, 50, 120),
    [(0.8, 0, 0.003), (0.5, 200, 0.007), (0.4, 400, 0.014)],
    200)

# Mid mountains (darker)
draw_mountains(draw, int(H * 0.62),
    (55, 35, 90),
    [(1.0, 50, 0.0025), (0.7, 300, 0.006), (0.5, 500, 0.012)],
    170)

# Near mountains (warm shadow)
draw_mountains(draw, int(H * 0.70),
    (40, 25, 60),
    [(1.2, 100, 0.003), (0.9, 350, 0.008), (0.6, 600, 0.015)],
    140)

# ── Ground ──
draw_mountains(draw, int(H * 0.78),
    (20, 40, 20),
    [(1.5, 0, 0.002), (0.8, 200, 0.005)],
    60)

# ── River ──
for x in range(0, W + 1, 4):
    offset = 20 * math.sin(x * 0.008) + 15 * math.sin(x * 0.015 + 100)
    river_y = H * 0.78 + offset
    w = int(12 + 8 * math.sin(x * 0.005))
    dist = abs(x - sun_x)
    brightness = max(0, 1 - dist / 350)
    r_col = int(180 + 75 * brightness)
    g_col = int(100 + 50 * brightness)
    b_col = int(30 + 20 * brightness)
    draw.line([(x, river_y - w), (x, river_y + w)], fill=(r_col, g_col, b_col))

# ── Pine trees ──
def draw_pine(draw, x, y, h, dark_shade=0):
    layers = 5
    layer_h = h // layers
    for i in range(layers):
        layer_w = int(h * 0.35 * (1 - i * 0.12))
        ly = y - i * layer_h
        shade = dark_shade + 15 * i
        gc = max(10 - shade, 0)
        draw.polygon([
            (x + random.randint(-2,2), ly - layer_h),
            (x - layer_w + random.randint(-1,1), ly),
            (x + layer_w + random.randint(-1,1), ly)
        ], fill=(max(15 - shade//3, 0), max(60 - shade, 0), max(15 - shade//3, 0)))
    draw.rectangle([x-3, y-5, x+3, y+10], fill=(50, 35, 20))

# Left tree group
for i in range(10):
    tx = 30 + i * 45 + random.randint(-10, 10)
    ty = H * 0.72 + random.randint(-10, 10)
    th = 50 + random.randint(-10, 25)
    draw_pine(draw, tx, ty, th)

# Right tree group
for i in range(8):
    tx = W - 60 - i * 50 + random.randint(-10, 10)
    ty = H * 0.73 + random.randint(-10, 10)
    th = 50 + random.randint(-10, 20)
    draw_pine(draw, tx, ty, th)

# ── Grass details ──
for _ in range(300):
    x = random.randint(0, W)
    y = H - random.randint(5, 50)
    h = random.randint(5, 12)
    shade = random.randint(20, 50)
    draw.line([(x, y), (x + random.randint(-3, 3), y - h)],
              fill=(10 + shade, 50 + shade, 10 + shade))

# ── Clouds ──
def draw_cloud(draw, cx, cy, size):
    for i in range(6):
        ox = random.randint(-size // 2, size // 2)
        oy = random.randint(-size // 4, size // 4)
        r = size // 2 + random.randint(-5, 5)
        alpha_val = random.randint(100, 180)
        cloud = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        cdraw = ImageDraw.Draw(cloud)
        cdraw.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                      fill=(255, 200, 120, alpha_val))
        nonlocal_img = img.convert('RGBA')
        nonlocal_img = Image.alpha_composite(nonlocal_img, cloud)
        # Can't use nonlocal properly, so let's do clouds differently

# Simpler clouds
cloud_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
cdraw = ImageDraw.Draw(cloud_img)
for cx, cy, sz in [(200, 120, 50), (320, 90, 40), (450, 110, 45),
                    (800, 80, 55), (950, 100, 40), (1050, 70, 35),
                    (150, 200, 35), (700, 130, 30)]:
    for _ in range(6):
        ox = random.randint(-sz // 2, sz // 2)
        oy = random.randint(-sz // 4, sz // 4)
        r = sz // 2 + random.randint(-4, 4)
        cdraw.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                      fill=(255, 200, 120, random.randint(100, 180)))
img = Image.alpha_composite(img.convert('RGBA'), cloud_img).convert('RGB')
draw = ImageDraw.Draw(img)

# ── Stars (subtle) ──
for _ in range(80):
    x = random.randint(0, W)
    y = random.randint(0, int(H * 0.25))
    sz = random.randint(1, 2)
    b = random.randint(150, 255)
    draw.ellipse([x, y, x + sz, y + sz], fill=(b, b, min(255, b + 30)))

# ── Birds (small V shapes) ──
for _ in range(5):
    bx = random.randint(W//4, 3*W//4)
    by = random.randint(int(H*0.25), int(H*0.40))
    sz = random.randint(4, 8)
    draw.line([(bx-sz, by+2), (bx, by)], fill=(30, 20, 30), width=1)
    draw.line([(bx, by), (bx+sz, by+2)], fill=(30, 20, 30), width=1)

# ── Smooth ──
img = img.filter(ImageFilter.SMOOTH)

# ── Save ──
import os
out_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'sunset_landscape.png')
img.save(out_path)
print("[OK] 画作已保存到: " + out_path)
print("[INFO] 尺寸: {}x{} 像素".format(img.size[0], img.size[1]))
print("[INFO] 主题: 山间日落")
