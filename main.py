from pybricks.hubs import PrimeHub
from pybricks.tools import wait, hub_menu
from pybricks.parameters import Axis
from Action import ParallelAction
from Robot import Robot
from missions import mission_list  # список миссий

hub = PrimeHub(front_side=Axis.Y, top_side=Axis.Z)
robot = Robot(hub)
odometry = robot.odometry_action()

while True:

    choice = hub_menu("1", "2", "3", "4", "5", "6", "7","8")
    print("Selected mission:", choice)

    index = int(choice) - 1

    mission_func = mission_list[index]
    actions = mission_func(robot)

    hub.speaker.beep()
    wait(100)

    while actions:
        odometry.update()   # одометрия всегда вычисляется параллельно
        for action in actions[:]:
            if action.update():
                actions.remove(action)
