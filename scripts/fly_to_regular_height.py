import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates
import sys
import tty, termios

# Constants
ARM_COMMAND = "ARM"
OFFBOARD_COMMAND = "OFFBOARD"
HOVER_COMMAND = "HOVER"
TARGET_HEIGHT = 1.5
LINEAR_VELOCITY = 0.4

# Global variables
drone_type = sys.argv[1]
num_drones = int(sys.argv[2])
control_type = sys.argv[3]
current_heights = [None] * int(sys.argv[2])
in_hover_modes = [False] * int(sys.argv[2])


def model_state_callback(msg):
    global current_heights
    for vehicle_id in range(num_drones):
        id = msg.name.index(drone_type + "_" + str(vehicle_id))
        current_height = msg.pose[id].position.z
        current_heights[vehicle_id] = current_height


def main():
    if len(sys.argv) < 4:
        print("Usage: python drone_control.py [drone_type] [num_drones] [control_type]")
        return

    rospy.init_node("drone_control")

    if control_type == "vel":
        cmd_pubs = []
        twist_pubs = []
        for i in range(num_drones):
            cmd_pub = rospy.Publisher(
                "/xtdrone/" + drone_type + "_" + str(i) + "/cmd", String, queue_size=4
            )
            twist_pub = rospy.Publisher(
                "/xtdrone/" + drone_type + "_" + str(i) + "/cmd_vel_flu",
                Twist,
                queue_size=1,
            )
            cmd_pubs.append(cmd_pub)
            twist_pubs.append(twist_pub)

    else:
        cmd_pubs = []
        acc_pubs = []
        for i in range(num_drones):
            cmd_pub = rospy.Publisher(
                "/xtdrone/" + drone_type + "_" + str(i) + "/cmd", String, queue_size=4
            )
            acc_pub = rospy.Publisher(
                "/xtdrone/" + drone_type + "_" + str(i) + "/cmd_accel_flu",
                Twist,
                queue_size=1,
            )
            cmd_pubs.append(cmd_pub)
            acc_pubs.append(acc_pub)

    # Create subscriber for getting model states
    rospy.Subscriber("/gazebo/model_states", ModelStates, model_state_callback)

    # Wait for the model state to be received
    rospy.wait_for_message("/gazebo/model_states", ModelStates)

    # Send offboard and arm commands to all drones
    print("cmd_pubs", len(cmd_pubs))
    print("twist_pubs", len(twist_pubs))
    for i in range(num_drones):
        rospy.sleep(0.02)
        cmd_pubs[i].publish(OFFBOARD_COMMAND)
        rospy.loginfo_once("OFFBOARD")
        rospy.sleep(0.02)  # Wait for offboard mode to be set
        cmd_pubs[i].publish(ARM_COMMAND)
        rospy.loginfo_once("ARM")
    for i in range(num_drones):
        rospy.sleep(0.02)
        cmd_pubs[i].publish(OFFBOARD_COMMAND)
        rospy.sleep(0.02)  # Wait for offboard mode to be set
        cmd_pubs[i].publish(ARM_COMMAND)

    # Control loop
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        twist = Twist()
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = LINEAR_VELOCITY
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        for i in range(num_drones):
            if current_heights[i] < TARGET_HEIGHT:
                # Send velocity command to ascend
                rospy.sleep(0.01)
                twist_pubs[i].publish(twist)
            else:
                # Enter hover mode
                twist = Twist()
                twist_pubs[i].publish(twist)
                if not in_hover_modes[i]:
                    rospy.sleep(0.01)
                    cmd_pubs[i].publish(HOVER_COMMAND)
                    in_hover_modes[i] = True
        rate.sleep()


if __name__ == "__main__":
    main()
