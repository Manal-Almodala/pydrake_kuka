#! /bin/bash
cd /pydrake_kuka/

# Launch a fake X-server in the background
Xvfb :100 -ac -screen 0 800x600x24 &

# Give that a sec to take effect
sleep 1

# Launch a complete robot context and execute some canned movement.
DISPLAY=:100 python kuka_cutting_sim.py -N 2 -T 5. --test
exit_status=$?
if [ ! $exit_status -eq 0 ]; then
  echo "Error code in kuka_pydrake_sim.py: " $exit_status
  exit $exit_status
fi

# Launch a complete robot context and execute some canned movement.
DISPLAY=:100 python kuka_flipping_sim.py -T 3. --test
exit_status=$?
if [ ! $exit_status -eq 0 ]; then
  echo "Error code in kuka_pydrake_sim.py: " $exit_status
  exit $exit_status
fi