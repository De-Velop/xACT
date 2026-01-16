from pybricks.hubs import PrimeHub
from pybricks.tools import wait, hub_menu
from pybricks.parameters import Axis, Port
from Action import ParallelAction, SequentialAction
from Robot import Robot
from missions import mission_list  # list of mission functions

# --- Initialize hub and robot ---
hub = PrimeHub(front_side=Axis.Y, top_side=Axis.Z)
robot = Robot(
    hub,
    left_port=Port.E,
    right_port=Port.A,
    arm_left_port=Port.F,
    arm_right_port=Port.B
)
odometry = robot.odometry_action()

while True:
    # --- Show menu on hub display ---
    choice = hub_menu("1", "2", "3", "4", "5", "6", "7", "8")
    print("Selected mission:", choice)

    # Convert the choice ("1"–"7") to index (0–6)
    index = int(choice) - 1

    # --- Get and run mission ---
    mission_func = mission_list[index]
    actions = mission_func(robot)

    # Always include odometry
    #actions.append(ParallelAction(robot, [robot.odometry_action()]))

    hub.speaker.beep()
    wait(500)

    # --- Run actions sequentially ---
    while actions:
        odometry.update()
        for action in actions[:]:
            if action.update():
                actions.remove(action)
