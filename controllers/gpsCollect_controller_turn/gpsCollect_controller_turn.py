from controller import Robot
import math

STRAIGHT_TIME_1 = 45.0
CURVE_TIME = 2.8
STRAIGHT_TIME_2 = 25.0
FORWARD_SPEED = 6.3
CURVE_LEFT_SPEED = 3.0
CURVE_RIGHT_SPEED = 6.0

def set_wheel_speeds(left_speed, right_speed,
                     fl_motor, fr_motor, bl_motor, br_motor):
    fl_motor.setVelocity(left_speed)
    bl_motor.setVelocity(left_speed)
    fr_motor.setVelocity(right_speed)
    br_motor.setVelocity(right_speed)
def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())
    fl_motor = robot.getDevice("front left wheel")
    fr_motor = robot.getDevice("front right wheel")
    bl_motor = robot.getDevice("back left wheel")
    br_motor = robot.getDevice("back right wheel")

    for m in [fl_motor, fr_motor, bl_motor, br_motor]:
        m.setPosition(float('inf'))
        m.setVelocity(0.0)
    gps = robot.getDevice("gps")
    gps.enable(timestep)
    compass = robot.getDevice("compass")
    compass.enable(timestep)
    log_file = open("gps_turn_log.txt", "w", encoding="utf-8")
    log_file.write("time x y z yaw\n")
    state = "STRAIGHT_1"
    start_time = robot.getTime()
    state_start_time = start_time

    while robot.step(timestep) != -1:
        current_time = robot.getTime()
        elapsed_state = current_time - state_start_time
        if state == "STRAIGHT_1":
            set_wheel_speeds(FORWARD_SPEED, FORWARD_SPEED,
                             fl_motor, fr_motor, bl_motor, br_motor)
            if elapsed_state > STRAIGHT_TIME_1:
                state = "CURVE_LEFT"
                state_start_time = current_time
        elif state == "CURVE_LEFT":
            set_wheel_speeds(CURVE_LEFT_SPEED, CURVE_RIGHT_SPEED,
                             fl_motor, fr_motor, bl_motor, br_motor)
            if elapsed_state > CURVE_TIME:
                state = "STRAIGHT_2"
                state_start_time = current_time
        elif state == "STRAIGHT_2":
            set_wheel_speeds(FORWARD_SPEED, FORWARD_SPEED,
                             fl_motor, fr_motor, bl_motor, br_motor)
            if elapsed_state > STRAIGHT_TIME_2:
                state = "STOP"
                set_wheel_speeds(0.0, 0.0,
                                 fl_motor, fr_motor, bl_motor, br_motor)
        elif state == "STOP":
            set_wheel_speeds(0.0, 0.0,
                             fl_motor, fr_motor, bl_motor, br_motor)
        gps_values = gps.getValues()
        x, y, z = gps_values[0], gps_values[1], gps_values[2]
        north = compass.getValues()
        yaw = math.atan2(north[0], north[2])
        log_file.write("{:.3f} {:.4f} {:.4f} {:.4f} {:.4f}\n".format(
            current_time - start_time, x, y, z, yaw
        ))
        log_file.flush()
    log_file.close()
if __name__ == "__main__":
    main()
