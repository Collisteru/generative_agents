#!/bin/bash

# Activate the main_env virtual environment
echo "Activating the virtual environment..."
source main_env/Scripts/activate

if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment. Exiting."
    exit 1
fi

echo "Virtual environment activated."

# Start the environment server in the background
echo "Starting the environment server..."
cd environment/frontend_server || exit
python manage.py runserver > /dev/null 2>&1 &
env_server_pid=$!

# Give the environment server some time to start
sleep 5

# Check if the environment server is running
if ps -p $env_server_pid > /dev/null
then
    echo "Environment server started successfully. Visit http://localhost:8000/ to check."
else
    echo "Failed to start the environment server. Exiting."
    exit 1
fi

# Start the simulation server in another background process
echo "Starting the simulation server..." 
echo ""
cd ../../reverie/backend_server || exit
python reverie.py > /dev/null 2>&1 &
sim_server_pid=$!

# Give the simulation server some time to start
sleep 2

# Interact with the simulation server
printf "Go to http://localhost:8000/simulator_home to access the simulation \n \n"
python reverie.py base_the_ville_isabella_maria_klaus

# Check if the simulation server is running
if ps -p $sim_server_pid > /dev/null
then
    echo "Simulation server started successfully."
else
    echo "Failed to start the simulation server. Exiting."
    exit 1
fi

# Keep both processes running until the user stops them
echo "Both servers are running. Press Ctrl+C to stop."

# Wait for Ctrl+C to stop both servers
trap "kill $env_server_pid $sim_server_pid; exit" SIGINT
wait
