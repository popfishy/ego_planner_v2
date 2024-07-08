import rospy
import sys
from quadrotor_msgs.msg import GoalSet

vehicle_type = sys.argv[1]
vehicle_id = sys.argv[2]
goal_point = GoalSet()


def goal_publisher():
    rospy.init_node(vehicle_type + "_" + vehicle_id + "_ego_swarm_goal")
    goal_pub = rospy.Publisher(
        vehicle_type + "_" + vehicle_id + "/move_base_simple/goal",
        GoalSet,
        queue_size=1,
    )

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        goal_point = GoalSet()
        goal_point.drone_id = int(vehicle_id)
        goal_point.goal = [float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]
        goal_pub.publish(goal_point)
        try:
            rate.sleep()
        except:
            continue


if __name__ == "__main__":
    try:
        goal_publisher()
    except rospy.ROSInterruptException:
        pass
