# === robot.py ===
# --- TODO: Выделить Actions в отдельный файл  --- 
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.tools import StopWatch, wait
from Action import Action
import umath

# --- TODO: Изменить на a = const  --- 
def speed_control(ratio, max_speed, min_speed=30):     
    direction = 1 if max_speed >= 0 else -1

    max_spd = abs(max_speed)
    min_spd = abs(min_speed)

    if ratio > 0.7:
        k = (min_spd - max_spd) / 0.3
        b = min_spd - k
        spd = k * ratio + b
    elif ratio < 0.3:
        k = (max_spd - min_spd) / 0.3
        spd = k * ratio + min_spd
    else:
        spd = max_spd
    return spd * direction


def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))


def angle_wrap(value):
    return (value + 180) % 360 - 180


class Robot:
    def __init__(self, hub: PrimeHub):
        print("\033[3J\033[H\033[2J", end="")   # очистить консоль
        self.hub = hub
        print(f"Voltage: {hub.battery.voltage()/1000} V")
        print(f"Current: {hub.battery.current()/1000} A")
        self.left = Motor(Port.E, Direction.COUNTERCLOCKWISE)
        self.right = Motor(Port.A)
        self.left.reset_angle(0)
        self.right.reset_angle(0)
        self.ArmLeft = Motor(Port.F)
        self.ArmRight = Motor(Port.B)
        self.ArmLeft.reset_angle(0)
        #self.ArmLeft.run_target(100, 0, Stop.HOLD, True)
        self.ArmRight.reset_angle(0)

        while not self.hub.imu.ready():
            pass
        self.hub.imu.reset_heading(0)

        self.X = 0.0
        self.Y = 0.0
        self.heading = 0.0
        self.velocity = 0.0

    def beep(self):
        self.hub.speaker.beep(880, 100)

    # === Одометрия ===
    def odometry_action(self):
        class Odom(Action):
            def __init__(inner, robot):
                super().__init__(robot)
                inner.prev_left = self.left.angle()
                inner.prev_right = self.right.angle()
                inner.prev_X = self.X
                inner.prev_Y = self.Y
                inner.timer = StopWatch()
                inner.last_time = inner.timer.time()

            def update(inner):
                self.heading = angle_wrap(self.hub.imu.heading())
                cur_left = self.left.angle()
                cur_right = self.right.angle()

                dL = cur_left - inner.prev_left
                dR = cur_right - inner.prev_right
                dist = (dL + dR) * 0.02721433057  # cm/deg 

                self.X += dist * umath.cos(umath.radians(self.heading))
                self.Y += dist * umath.sin(umath.radians(self.heading))

                inner.prev_left = cur_left
                inner.prev_right = cur_right

                # вычисление скорости (скалярная) 
                t = inner.timer.time()
                dt = (t - inner.last_time) / 1000
                if dt > 0.05:
                    dx = self.X - inner.prev_X
                    dy = self.Y - inner.prev_Y
                    self.velocity = umath.sqrt(dx*dx + dy*dy) / dt
                    inner.prev_X, inner.prev_Y = self.X, self.Y
                    inner.last_time = t

                return False
        return Odom(self)

    # === Езда до точки ===
    def drive_to_point_action(self, _X, _Y, speed=90):
        class DriveToPointAction(Action):
            def on_start(inner_self):
                inner_self.start_x = self.X
                inner_self.start_y = self.Y
                inner_self.timer = StopWatch()
                inner_self.last_time = inner_self.timer.time()

                inner_self.direction = 1 if speed >= 0 else -1

                inner_self.prev_error = 0
                inner_self.integral = 0

                inner_self.dx = _X - inner_self.start_x
                inner_self.dy = _Y - inner_self.start_y
                inner_self.total_dist = umath.sqrt(inner_self.dx**2 + inner_self.dy**2)
                inner_self.target_heading_abs = umath.degrees(umath.atan2(inner_self.dy, inner_self.dx))

            def update(inner_self):
                current_heading = self.heading

                vec_to_robot_x = self.X - inner_self.start_x
                vec_to_robot_y = self.Y - inner_self.start_y
                proj_len = (vec_to_robot_x * inner_self.dx + vec_to_robot_y * inner_self.dy) / inner_self.total_dist
                dist_remain = inner_self.total_dist - proj_len

                if dist_remain <= 0.05:  
                    self.left.stop()
                    self.right.stop()
                    self.beep()
                    print(f"X = {self.X:.2f}, Y = {self.Y:.2f}, H = {self.heading:.2f}")
                    return True

                signed_d = (inner_self.dy * (self.X - inner_self.start_x) - inner_self.dx * (self.Y - inner_self.start_y)) / inner_self.total_dist

                lookahead = max(3, self.velocity * 0.3 + 3)
                target_heading = umath.degrees(umath.atan2(signed_d, lookahead))
                effective_heading = (current_heading + 180) % 360 if inner_self.direction == -1 else current_heading
                heading_error = angle_wrap(target_heading - (effective_heading - inner_self.target_heading_abs))

                current_time = inner_self.timer.time()
                dt = (current_time - inner_self.last_time) / 1000
                inner_self.last_time = current_time

                kp = 4.0
                ki = 0.6
                kd = 0.2

                inner_self.integral = inner_self.integral * 0.7 + heading_error  
                derivative = angle_wrap(heading_error - inner_self.prev_error) / dt if dt > 0 else 0
                inner_self.prev_error = heading_error

                correction = kp * heading_error + ki * inner_self.integral + kd * derivative

                ratio = proj_len / inner_self.total_dist
                current_speed = speed_control(ratio, speed)

                self.left.dc(current_speed + correction)
                self.right.dc(current_speed - correction)

                return False

        return DriveToPointAction(self)

    #  --- TODO: дублирует код, написать через drive_to_point  --- 
    def straight_action(self, _distance, speed=90):
        class StraightAction(Action):
            def on_start(inner_self):
                inner_self.start_x = self.X
                inner_self.start_y = self.Y
                inner_self.timer = StopWatch()
                inner_self.last_time = inner_self.timer.time()

                inner_self.direction = 1 if speed >= 0 else -1

                inner_self.prev_error = 0
                inner_self.integral = 0

                _X = self.X + (umath.cos(umath.radians(self.heading)) * _distance) * (-1 if speed < 0 else 1)
                _Y = self.Y + (umath.sin(umath.radians(self.heading)) * _distance) * (-1 if speed < 0 else 1)

                inner_self.dx = _X - inner_self.start_x
                inner_self.dy = _Y - inner_self.start_y
                inner_self.total_dist = umath.sqrt(inner_self.dx**2 + inner_self.dy**2)
                inner_self.target_heading_abs = umath.degrees(umath.atan2(inner_self.dy, inner_self.dx))

            def update(inner_self):
                current_heading = self.heading

                vec_to_robot_x = self.X - inner_self.start_x
                vec_to_robot_y = self.Y - inner_self.start_y
                proj_len = (vec_to_robot_x * inner_self.dx + vec_to_robot_y * inner_self.dy) / inner_self.total_dist
                dist_remain = inner_self.total_dist - proj_len

                if dist_remain <= 0.05:  
                    self.left.stop()
                    self.right.stop()
                    self.beep()
                    print(f"X = {self.X:.2f}, Y = {self.Y:.2f}, H = {self.heading:.2f}")
                    return True

                signed_d = (inner_self.dy * (self.X - inner_self.start_x) - inner_self.dx * (self.Y - inner_self.start_y)) / inner_self.total_dist

                lookahead = max(3, self.velocity * 0.3 + 3)
                target_heading = umath.degrees(umath.atan2(signed_d, lookahead))
                effective_heading = (current_heading + 180) % 360 if inner_self.direction == -1 else current_heading
                heading_error = angle_wrap(target_heading - (effective_heading - inner_self.target_heading_abs))

                current_time = inner_self.timer.time()
                dt = (current_time - inner_self.last_time) / 1000
                inner_self.last_time = current_time

                kp = 4.0
                ki = 0.6
                kd = 0.2

                inner_self.integral = inner_self.integral * 0.7 + heading_error  
                derivative = angle_wrap(heading_error - inner_self.prev_error) / dt if dt > 0 else 0
                inner_self.prev_error = heading_error

                correction = kp * heading_error + ki * inner_self.integral + kd * derivative

                ratio = proj_len / inner_self.total_dist
                current_speed = speed_control(ratio, speed)

                self.left.dc(current_speed + correction)
                self.right.dc(current_speed - correction)

                return False

        return StraightAction(self)

    def turn_to_heading_action(self, target_heading, max_speed=50):
        class Turn(Action):
            def on_start(inner):
                inner.kP = 7.0
                inner.kI = 100
                inner.kD = 0.5
                inner.integral = 0
                inner.prev_error = 0
                inner.timer = StopWatch()  
                inner.last_time = inner.timer.time()
                inner.error_within_threshold_since = inner.last_time

            def update(inner):
                error = angle_wrap(target_heading - self.heading)
                now = inner.timer.time() 
                dt = (now - inner.last_time) / 1000
                if now > 100: inner.last_time = now

                if abs(error) < 5: inner.integral = clamp(inner.integral * 0.99 + error * dt, -50, 50)
                derivative = angle_wrap(error - inner.prev_error) / dt if dt > 0 else 0
                inner.prev_error = error

                U = inner.kP * error + inner.kI * inner.integral + inner.kD * derivative
                if 0 < abs(U) < 20: U = 20 if U > 0 else -20
                self.left.dc(clamp(U, -max_speed, max_speed))
                self.right.dc(clamp(-U, -max_speed, max_speed))

                if abs(error) < 2:
                    if now - inner.error_within_threshold_since > 100:
                        self.left.stop()
                        self.right.stop()
                        print(f"X = {self.X:.2f}, Y = {self.Y:.2f}, H = {self.heading:.2f}")
                        self.beep()
                        return True
                else:
                    inner.error_within_threshold_since = now

                return False

        return Turn(self)

    def arm_action(self, Arm_Name, speed, angle, stop = Stop.HOLD, waiting = True):
        class ArmAction(Action):
            def on_start(inner):
                if Arm_Name == "L": self.Arm = self.ArmLeft
                else: self.Arm = self.ArmRight

            def update(inner):
                self.Arm.run_angle(speed, angle, stop, waiting)
                if waiting: self.beep()
                return True
        return ArmAction(self)

    def single_wheel_action(self, Wheel_Name, speed, angle, stop = Stop.HOLD, waiting = True):
        class SingleWheelAction(Action):
            def on_start(inner):
                if Wheel_Name == "L": self.Wheel = self.left
                else: self.Wheel = self.right

            def update(inner):
                self.Wheel.run_angle(speed, angle, stop, waiting)
                if waiting: self.beep()
                return True
        return SingleWheelAction(self)

    def wall_bump(self, WallName, speed, waitTime = 0):
        class WallBumpAction(Action):
            def on_start(inner_self):
                inner_self.timer = StopWatch()

            def update(inner_self):
                self.left.dc(speed)
                self.right.dc(speed)
                if inner_self.timer.time() >= waitTime * 1000:
                    self.beep()
                    if WallName == "U":
                        self.X = 105.2
                        self.hub.imu.reset_heading(180)
                    else:
                        self.X = 0
                        self.hub.imu.reset_heading(0)
                    return True
                return False

        return WallBumpAction(self)

    def arm_dc(self, Arm_Name, speed, waitTime = 0):
        class ArmDCAction(Action):
            def on_start(inner_self):
                if Arm_Name == "L": self.Arm = self.ArmLeft
                else: self.Arm = self.ArmRight
                inner_self.timer = StopWatch()

            def update(inner_self):
                self.Arm.dc(speed)
                if inner_self.timer.time() >= waitTime * 1000:
                    self.beep()
                    return True
                return False

        return ArmDCAction(self)

    def sound_action(self):
        class Sound(Action):
            def update(inner): 
                self.hub.speaker.beep(880, 100)
                return True
        return Sound(self)

    def reset_odometry_action(self, _X, _Y, heading): 
        class ResetOdometryAction(Action):
            def update(inner_self):
                self.X = _X
                self.Y = _Y
                self.hub.imu.reset_heading(heading)
            
                return True
        return ResetOdometryAction(self)
