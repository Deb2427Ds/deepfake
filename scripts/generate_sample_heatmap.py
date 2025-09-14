# scripts/generate_sample_heatmap.py
from PIL import Image, ImageDraw, ImageFilter
import math
import os

OUT = "backend_static_heatmap.png"
W, H = 1024, 576
img = Image.new("RGBA", (W, H), (30, 30, 30, 255))
draw = ImageDraw.Draw(img)

cx, cy = W // 2, H // 2
r = 160
for i in range(28):
    intensity = 120 + i * 4
    bbox = [cx - r - i, cy - r - i, cx + r + i, cy + r + i]
    draw.ellipse(bbox, outline=(intensity, 20, 20, 140))

for x in range(6):
    dx = cx + int(math.cos(x) * 120)
    dy = cy + int(math.sin(x * 1.3) * 80)
    draw.ellipse([dx - 80, dy - 80, dx + 80, dy + 80], fill=(255, 60, 60, 100))

img = img.filter(ImageFilter.GaussianBlur(6))
img.save(OUT)
print("Saved", OUT)
