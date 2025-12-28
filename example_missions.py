from Action import SequentialAction, ParallelAction
from pybricks.hubs import PrimeHub
from pybricks.tools import wait, hub_menu

def mission1(robot):
    return [
        SequentialAction(robot, [
            robot.reset_odometry_action(0, 0, 0),
            robot.reset_odometry_action(0, 0, 0),
            robot.arm_dc("L", 0, 1),
            robot.arm_dc("R", 50, 1),
            robot.arm_dc("L", 50),
            robot.drive_to_point_action(_X = 60, _Y = 0, speed = 100),
            robot.arm_dc("L", -100),
            robot.drive_to_point_action(_X = 64, _Y = 0, speed = 40),
            robot.drive_to_point_action(_X = 56, _Y = 0, speed = -40),
            robot.drive_to_point_action(_X = 60, _Y = 0, speed = 40),
            robot.arm_dc("L", 70, 1),
            robot.arm_dc("L", 0),
            robot.turn_to_heading_action(50),
            robot.straight_action(18, speed = 50),
            robot.turn_to_heading_action(315),
            robot.straight_action(15, speed = 50),
            robot.arm_action("R", -50, 75),
            robot.straight_action(20, speed = -50),
            robot.turn_to_heading_action(10),
            robot.straight_action(75, speed = -75),
        ])
    ]

def mission2(robot):
    return [
        SequentialAction(robot, [
            robot.reset_odometry_action(0, 0, 0),
            robot.arm_dc("L", -40),
            robot.straight_action(40, speed=80),
            robot.turn_to_heading_action(180),
            robot.straight_action(65, speed=-80),
            robot.wall_bump("U", -50, 1),
            robot.straight_action(15, speed=30),
            robot.turn_to_heading_action(79),
            robot.arm_action("L", 60, 80),
            robot.straight_action(12.2, speed=30),
            wait(2500),
            robot.arm_action("L", -40, 30),
            wait(1000),
            robot.straight_action(16.2, -50),
            wait(200),
            robot.arm_action("L", -20, 40),
            robot.turn_to_heading_action(0),
            robot.straight_action(90, -80),
        ])
    ]

def mission3(robot):
    return [
        SequentialAction(robot, [
            robot.reset_odometry_action(0, 0, 0),
            robot.straight_action(42, 70),
            robot.straight_action(49, -80),
             ])
    ]

def mission4(robot):
    return [
        SequentialAction(robot, [
        robot.reset_odometry_action(0, 0, 0),

        robot.straight_action(28 , speed=60),
        robot.turn_to_heading_action(-90),

        robot.straight_action(74, speed=80),
        robot.turn_to_heading_action(180),
        robot.straight_action(6.2, speed=40),
        robot.single_wheel_action("R", 70, 37),
        robot.arm_dc("L", -500, waitTime=3.5),

        robot.straight_action(10, -50),
        robot.arm_dc("L", 0),
        robot.turn_to_heading_action(110),
        robot.straight_action(65, 80),
        ])
    ]

def mission5(robot):
    return [
        SequentialAction(robot, [
        robot.straight_action(73, 80),
        robot.single_wheel_action("R", 500, 340),
        robot.single_wheel_action("R", -500, 180),

        robot.turn_to_heading_action(-90),
        robot.straight_action(32, -50),
        robot.turn_to_heading_action(0),
        robot.straight_action(90, -90),        
        ])
    ]

def mission6(robot):
    return [
        SequentialAction(robot, [
            robot.reset_odometry_action(0, 0, 0),
            robot.arm_dc("L", -800),
            robot.straight_action(45, speed=60),
            robot.turn_to_heading_action(-50),
            robot.straight_action(15, speed=60),

            wait(500),
            robot.straight_action(5.2, speed=-60),
            robot.turn_to_heading_action(-80),
            robot.straight_action(5, speed=70),
            robot.straight_action(10, speed=-70),

            robot.turn_to_heading_action(-40),
            robot.straight_action(50, speed=-70),
        ])
    ]    

def mission7(robot):
    return [
        SequentialAction(robot, [
            robot.reset_odometry_action(0, 0, 0),
            robot.straight_action(30, speed=60),
            robot.turn_to_heading_action(-90),
            robot.straight_action(39, 55),
            robot.turn_to_heading_action(-20),
            robot.straight_action(2.1, 55),
            wait(1000),
            robot.arm_action("R", 500, -55),
            wait(500),
            robot.arm_action("R", 500, 55),
            robot.turn_to_heading_action(-44),
            robot.straight_action(12, -65),
            robot.arm_action("R", 500, -70),
            robot.straight_action(8, -80),
            wait(200),

            robot.turn_to_heading_action(-70),
            robot.straight_action(50, -80),
        ])
    ]

def mission8(robot):
    return [
        SequentialAction(robot, [
            robot.arm_dc("L", -1000),
            robot.straight_action(26, 70),
            robot.turn_to_heading_action(-90),
            robot.straight_action(75, 80),
            robot.turn_to_heading_action(-33),
            robot.straight_action(15, 60),
            robot.arm_dc("L", 0),
            wait(200),
            robot.arm_action("L", 1000, 80),
            robot.turn_to_heading_action(-70),
            robot.straight_action(90, -80),
        ])
    ]

def mission9(robot):
    return [
        SequentialAction(robot, [
            robot.reset_odometry_action(0, 0, 0),
            robot.straight_action(30.5, speed=60),
            robot.turn_to_heading_action(-90),
            robot.turn_to_heading_action(-10),
            wait(300), 
            robot.arm_action("R", 700, -50),
            robot.straight_action(15, -50),
            robot.straight_action(1, 50),
            robot.arm_action("R", 600, 40),
            robot.straight_action(50, -50),
        ])
    ]

mission_list = [mission1, mission2, mission3, mission4, mission5, mission6, mission7, mission8, mission9 ]