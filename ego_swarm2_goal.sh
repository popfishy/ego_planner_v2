#!/bin/bash
    # python3 ego_swarm_goal.py iris 0 7 4 0&
    # python3 ego_swarm_goal.py iris 1 8 -5 0&
    # python3 ego_swarm_goal.py iris 2 3 -3 0&
    # python3 ego_swarm_goal.py iris 3 -7 -8 0
while(true)
do
    python3 ego_swarm2_goal.py iris 0 7 4 0&
    python3 ego_swarm2_goal.py iris 1 8 -5 0&
    python3 ego_swarm2_goal.py iris 2 3 -3 0&
    python3 ego_swarm2_goal.py iris 3 -7 -6 0
done
