import math
import os

INPUT_LOG = os.path.join(os.path.dirname(__file__), "gps_turn_log.txt")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__),
                           "..", "simple_follow", "follow_path.txt")
MIN_DIST = 0.4

def main():
    points = []
    with open(INPUT_LOG, "r", encoding="utf-8") as f:
        header = f.readline()
        prev_x = None
        prev_y = None
        for line in f:
            line = line.strip()
            if not line:
                continue
            t_str, x_str, y_str, z_str, yaw_str = line.split()
            x = float(x_str)
            y = float(y_str)
            if prev_x is None:
                points.append((x, y))
                prev_x, prev_y = x, y
            else:
                dx = x - prev_x
                dy = y - prev_y
                dist = math.hypot(dx, dy)
                if dist >= MIN_DIST:
                    points.append((x, y))
                    prev_x, prev_y = x, y
                    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for x, y in points:
            f.write(f"{x:.4f} {y:.4f}\n")
if __name__ == "__main__":
    main()
