from controller import Robot

STRAIGHT1_TIME = 67.0
TURN1_TIME = 2.18
STRAIGHT2_TIME = 88.0
TURN2_TIME = 2.18
STRAIGHT3_TIME = 395.0
TURN3_TIME = 2.15
STRAIGHT4_TIME = 60.0
FORWARD_SPEED = 6.5
TURN_SPEED = 2.0

LOG_FILE = "gps_turn_log.txt"
def set_wheel_speeds(left_speed, right_speed, fl, fr, bl, br):
    fl.setVelocity(left_speed)
    bl.setVelocity(left_speed)
    fr.setVelocity(right_speed)
    br.setVelocity(right_speed)

def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())
    fl = robot.getDevice("front left wheel")
    fr = robot.getDevice("front right wheel")
    bl = robot.getDevice("back left wheel")
    br = robot.getDevice("back right wheel")
    for m in [fl, fr, bl, br]:
        m.setPosition(float('inf'))
        m.setVelocity(0.0)
    gps = robot.getDevice("gps")
    gps.enable(timestep)
    log = open(LOG_FILE, "w")
    log.write("time  x  y  z  yaw\n")
    state = "STRAIGHT1"
    state_start_time = robot.getTime()
   
    while robot.step(timestep) != -1:
        t = robot.getTime()
        pos = gps.getValues()
        x, y, z = pos[0], pos[1], pos[2]
        log.write(f"{t:.3f} {x:.4f} {y:.4f} {z:.4f} 0.0000\n")
        log.flush()
        if state == "STRAIGHT1":
            set_wheel_speeds(FORWARD_SPEED, FORWARD_SPEED, fl, fr, bl, br)
            if t - state_start_time >= STRAIGHT1_TIME:
                state = "TURN1"
                state_start_time = t
                print("TURN1")
        elif state == "TURN1":
            set_wheel_speeds(-TURN_SPEED, TURN_SPEED, fl, fr, bl, br)
            if t - state_start_time >= TURN1_TIME:
                state = "STRAIGHT2"
                state_start_time = t
                print("STRAIGHT2")
        elif state == "STRAIGHT2":
            set_wheel_speeds(FORWARD_SPEED, FORWARD_SPEED, fl, fr, bl, br)
            if t - state_start_time >= STRAIGHT2_TIME:
                state = "TURN2"
                state_start_time = t
                print("TURN2")
        elif state == "TURN2":
            set_wheel_speeds(-TURN_SPEED, TURN_SPEED, fl, fr, bl, br)
            if t - state_start_time >= TURN2_TIME:
                state = "STRAIGHT3"
                state_start_time = t
                print("STRAIGHT3")
        elif state == "STRAIGHT3":
            set_wheel_speeds(FORWARD_SPEED, FORWARD_SPEED, fl, fr, bl, br)
            if t - state_start_time >= STRAIGHT3_TIME:
                state = "TURN3"
                state_start_time = t
                print("TURN3")
        elif state == "TURN3":
            set_wheel_speeds(-TURN_SPEED, TURN_SPEED, fl, fr, bl, br)
            if t - state_start_time >= TURN3_TIME:
                state = "STRAIGHT4"
                state_start_time = t
                print("STRAIGHT4")
        elif state == "STRAIGHT4":
            set_wheel_speeds(FORWARD_SPEED, FORWARD_SPEED, fl, fr, bl, br)
            if t - state_start_time >= STRAIGHT4_TIME:
                set_wheel_speeds(0.0, 0.0, fl, fr, bl, br)
                state = "STOP"
                print("STOP")
        elif state == "STOP":
            set_wheel_speeds(0.0, 0.0, fl, fr, bl, br)
    log.close()
if __name__ == "__main__":
    main()
