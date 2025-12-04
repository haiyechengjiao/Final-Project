from controller import Robot
import os
import math

TIME_STEP = 32
BASE_SPEED = 4.0
MAX_SPEED  = 6.0
KP_TURN    = 3.0
DIST_THR   = 0.4

def load_path():
    path_file = os.path.join(os.path.dirname(__file__), "follow_path.txt")
    pts = []
    with open(path_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            xs, ys = line.split()
            pts.append((float(xs), float(ys)))
    return pts
def main():
    robot = Robot()
    gps = robot.getDevice("gps")
    gps.enable(TIME_STEP)
    names = ["front left wheel", "front right wheel",
             "back left wheel",  "back right wheel"]
    motors = []
    for n in names:
        m = robot.getDevice(n)
        m.setPosition(float('inf'))
        m.setVelocity(0.0)
        motors.append(m)
    path_points = load_path()
    current_wp = 0
    prev_x = None
    prev_y = None
    yaw_est = 0.0     
    while robot.step(TIME_STEP) != -1:
        if current_wp >= len(path_points):
            for m in motors:
                m.setVelocity(0.0)
            continue
        gps_vals = gps.getValues()
        x = gps_vals[0]    
        y = gps_vals[1]    
        if prev_x is not None:
            dx_pos = x - prev_x
            dy_pos = y - prev_y
            if math.hypot(dx_pos, dy_pos) > 1e-3:
                yaw_est = math.atan2(dy_pos, dx_pos)
        prev_x, prev_y = x, y
        tx, ty = path_points[current_wp]
        dx = tx - x
        dy = ty - y
        dist = math.hypot(dx, dy)
        if dist < DIST_THR:
            current_wp += 1
            continue
        target_heading = math.atan2(dy, dx)
        err = target_heading - yaw_est
        while err > math.pi:
            err -= 2 * math.pi
        while err < -math.pi:
            err += 2 * math.pi
        turn = KP_TURN * err
        left  = BASE_SPEED - turn
        right = BASE_SPEED + turn
        left  = max(-MAX_SPEED, min(MAX_SPEED, left))
        right = max(-MAX_SPEED, min(MAX_SPEED, right))
        motors[0].setVelocity(left)
        motors[2].setVelocity(left)
        motors[1].setVelocity(right)
        motors[3].setVelocity(right)
if __name__ == "__main__":
    main()
