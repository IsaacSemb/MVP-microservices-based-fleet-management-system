#!/bin/bash

# Name the tmux session
SESSION="msa_project"

# Virtual environment path
VENV_DIR="/mnt/c/Users/ikesemb/Desktop/MASTERS\\ PROJECT/001-DISSERTATION/000_proof_of_concept_stuff/MSA_ITERATION_3/.venv/Scripts"

# List of services mapped to numbers
SERVICES=(
  "service1_driver_management"
  "service2_vehicle_management"
  "service3_assignments"
  "service4_maintenance_repairs"
  "service5_scheduling"
  "service6_fuel_consumption_service"
  "service7_tasks_services"
)

# Ensure 2 arguments are provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <service_number1> <service_number2>"
  echo "Example: $0 1 2"
  echo "Available services:"
  for i in "${!SERVICES[@]}"; do
    echo "$((i + 1)) - ${SERVICES[i]}"
  done
  exit 1
fi

# Map arguments to services
SERVICE1=${SERVICES[$1-1]}
SERVICE2=${SERVICES[$2-1]}
# SERVICE3=${SERVICES[$3-1]}
# SERVICE4=${SERVICES[$4-1]}

# Kill all existing tmux sessions first
tmux kill-server

# Start a new detached tmux session
tmux new-session -d -s $SESSION

# Split the tmux window into four panes
tmux split-window -h    # Split into two panes (horizontal split)
# tmux split-window -v    # Split the left pane into top and bottom (vertical split)
# tmux select-pane -t 0   # Go back to the first pane
# tmux split-window -v    # Split the right pane into top and bottom (vertical split)

# Define the commands for each service
CMD1="$VENV_DIR/python.exe \"C:/Users/ikesemb/Desktop/MASTERS PROJECT/001-DISSERTATION/000_proof_of_concept_stuff/MSA_ITERATION_3/services/$SERVICE1/app.py\""
CMD2="$VENV_DIR/python.exe \"C:/Users/ikesemb/Desktop/MASTERS PROJECT/001-DISSERTATION/000_proof_of_concept_stuff/MSA_ITERATION_3/services/$SERVICE2/app.py\""
# CMD3="$VENV_DIR/python.exe \"C:/Users/ikesemb/Desktop/MASTERS PROJECT/001-DISSERTATION/000_proof_of_concept_stuff/MSA_ITERATION_3/services/$SERVICE3/app.py\""
# CMD4="$VENV_DIR/python.exe \"C:/Users/ikesemb/Desktop/MASTERS PROJECT/001-DISSERTATION/000_proof_of_concept_stuff/MSA_ITERATION_3/services/$SERVICE4/app.py\""

# Send the commands to the respective panes
tmux send-keys -t 0 "$CMD1" C-m
tmux send-keys -t 1 "$CMD2" C-m
tmux send-keys -t 2 "$CMD3" C-m
tmux send-keys -t 3 "$CMD4" C-m

# Attach the tmux session
tmux attach-session -t $SESSION
