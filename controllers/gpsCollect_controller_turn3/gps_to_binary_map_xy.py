import numpy as np
import matplotlib.pyplot as plt

DATA_FILE = "gps_turn_log.txt"
IMG_SIZE = 800

def bresenham_line(x0, y0, x1, y1):
    points = []
    x0 = int(round(x0));  y0 = int(round(y0))
    x1 = int(round(x1));  y1 = int(round(y1))
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        points.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return points

def load_gps_xy(path):
    data = np.loadtxt(path, skiprows=1)
    xs = data[:, 1]  
    ys = data[:, 2]   
    return xs, ys

def build_binary_map(xs, ys, size=IMG_SIZE):
    img = np.zeros((size, size), dtype=np.uint8)
    if len(xs) < 2:
        return img
    min_x, max_x = xs.min(), xs.max()
    min_y, max_y = ys.min(), ys.max()
    margin = int(size * 0.1)
    span_x = max(1e-9, max_x - min_x)
    span_y = max(1e-9, max_y - min_y)
    norm_xs = margin + (xs - min_x) / span_x * (size - 1 - 2 * margin)
    norm_ys = margin + (ys - min_y) / span_y * (size - 1 - 2 * margin)
    prev_x, prev_y = norm_xs[0], norm_ys[0]
    for x_f, y_f in zip(norm_xs[1:], norm_ys[1:]):
        for (ix, iy) in bresenham_line(prev_x, prev_y, x_f, y_f):
            if 0 <= ix < size and 0 <= iy < size:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        xx, yy = ix + dx, iy + dy
                        if 0 <= xx < size and 0 <= yy < size:
                            img[yy, xx] = 255
        prev_x, prev_y = x_f, y_f
    return img
def main():
    xs, ys = load_gps_xy(DATA_FILE)
    img = build_binary_map(xs, ys)
    plt.figure(figsize=(6, 6))
    plt.imshow(img, cmap="gray", origin="lower")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("binary_map_xy.png", dpi=200, bbox_inches="tight")
    plt.show()
if __name__ == "__main__":
    main()
