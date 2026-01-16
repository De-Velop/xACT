from Action import SequentialAction, ParallelAction

def mission1(robot):
    return [
        SequentialAction(robot, [
            robot.reset_odometry_action(0, 0, 0),
            ParallelAction(robot, [
                robot.drive_to_point_action(50, 0, 70),
                robot.arm_action('L', 50, 50),
            ]), 
            robot.single_wheel_action('R', 70, 60),
        ])
    ]

def mission2(robot):
    return [
        SequentialAction(robot, [
            robot.straight_action(82, 100),
            robot.single_wheel_action('L', -60, 200),
            ParallelAction(robot, [
                robot.straight_action(12, 70),
                robot.arm_action('R', 60, 100),
            ]), 
            robot.wait_action(500),
        ])
    ]

mission_list = [mission1, mission2]
