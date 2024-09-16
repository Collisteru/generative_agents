import subprocess
import time
import os

def activate_virtual_env():
    """Activates the main_env virtual environment."""
    # Adjust this path to point to the virtual environment activation script
    activate_script = os.path.join("main_env", "Scripts", "activate")
    activate_command = "source main_env/Scripts/activate"
    
    subprocess.call(activate_command, shell=True)
    print("Activating the virtual environment...")
    
    time.sleep(5) # Wait for the venv to activate

    print("Virtual environment activated.")

def start_environment_server():
    """Starts the Django environment server."""
    print("Starting environment server...")
    # Navigate to environment/frontend_server and run the server
    env_server = subprocess.Popen(
        ["python", "manage.py", "runserver"],
        cwd="environment/frontend_server",  # Change to directory where manage.py is located
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        
    )
    time.sleep(5)  # Wait for the server to start
    print("Environment server started. Visit http://localhost:8000/ to check.")

    return env_server

def start_simulation_server():
    """Starts the simulation server and handles input for forked and new simulations."""
    print("Starting simulation server...")
    # Navigate to reverie/backend_server and run reverie.py
    sim_server = subprocess.Popen(
        ["python", "reverie.py"],
        cwd="reverie/backend_server",  # Change to the backend server directory
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # Send input for forked simulation
    sim_server.stdin.write("base_the_ville_isabella_maria_klaus\n")
    sim_server.stdin.flush()
    # Send input for new simulation
    sim_server.stdin.write("test-simulation\n")
    sim_server.stdin.flush()
    
    print("Simulation server started. Input provided for forked simulation and new simulation.")

    return sim_server

if __name__ == "__main__":
    try:
        # Step 1: Activate virtual environment
        activate_virtual_env()

        # Step 2: Start both servers
        env_process = start_environment_server()
        sim_process = start_simulation_server()

        # Keep both servers running
        print("Both servers are running. Press Ctrl+C to stop.")
        while True:
            time.sleep(10)

    except KeyboardInterrupt:
        print("Shutting down servers...")
        env_process.terminate()
        sim_process.terminate()
        print("Servers stopped.")
