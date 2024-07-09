#!/bin/bash
    # env:ego_swarm.world  0:(-8,5,0)->(7,4,0) 1:(-8,5,0)->(8,-5,0) 2:(8,4,0)->(3,-3,0) 3:(7,-8,0)->(-7,-8,0)
    # env:dynamic_tree_without_person.world 
    # python3 ego_swarm_goal.py iris 0 7 4 0&
    # python3 ego_swarm_goal.py iris 1 8 -5 0&
    # python3 ego_swarm_goal.py iris 2 3 -3 0&
    # python3 ego_swarm_goal.py iris 3 -7 -8 0
while(true)
do
    python3 ego_swarm2_goal.py iris 0 12 -16 1.5&
    python3 ego_swarm2_goal.py iris 5 12 -12 1.5&
    python3 ego_swarm2_goal.py iris 8 12 -8 1.5&
    python3 ego_swarm2_goal.py iris 3 12 -4 1.5&
    python3 ego_swarm2_goal.py iris 2 12 0 1.5&
    python3 ego_swarm2_goal.py iris 1 12 4 1.5&
    python3 ego_swarm2_goal.py iris 7 12 8 1.5&
    python3 ego_swarm2_goal.py iris 4 12 12 1.5&
    python3 ego_swarm2_goal.py iris 6 12 16 1.5
done
