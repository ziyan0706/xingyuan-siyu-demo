# -*- coding: utf-8 -*-
"""在截图上画一个干净的红箭头。
用法（在别的脚本里 import）：
    from redarrow import draw_arrow
    draw_arrow(im, sx, sy, ex, ey)
"""
import math
from PIL import ImageDraw

RED = (255, 59, 48)


def draw_arrow(im, sx, sy, ex, ey, color=RED, width=5, head_l=26, head_w=9):
    """从 (sx,sy) 指向 (ex,ey)：细直线 + 干净的三角头。"""
    d = ImageDraw.Draw(im)
    ang = math.atan2(ey - sy, ex - sx)
    # 线在头部之前收住，避免和三角头叠出粗糙的拐角
    bx = ex - head_l * 0.8 * math.cos(ang)
    by = ey - head_l * 0.8 * math.sin(ang)
    d.line([(sx, sy), (bx, by)], fill=color, width=width)
    p2 = (ex - head_l * math.cos(ang) + head_w * math.sin(ang),
          ey - head_l * math.sin(ang) - head_w * math.cos(ang))
    p3 = (ex - head_l * math.cos(ang) - head_w * math.sin(ang),
          ey - head_l * math.sin(ang) + head_w * math.cos(ang))
    d.polygon([(ex, ey), p2, p3], fill=color)
    return im


def red_pixels(im, base=None):
    """统计红像素；给了 base 就只统计新增的（用来核对箭头位置）。"""
    px, W, H = im.load(), im.width, im.height
    bp = base.load() if base else None

    def isred(c):
        return c[0] > 200 and c[1] < 100 and c[2] < 100

    pts = [(x, y) for y in range(H) for x in range(W)
           if isred(px[x, y]) and (bp is None or not isred(bp[x, y]))]
    if not pts:
        return 0, None
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return len(pts), (min(xs), max(xs), min(ys), max(ys))
