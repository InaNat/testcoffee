import subprocess
import signal
import os
import time
import platform
from send_req_llama import LlamaPrompt

processes = []

def run_in_new_terminal(cmd, title=None):
    """Run a command in a new terminal window."""
    system = platform.system()
    if system == "Linux":
        args = ["gnome-terminal"]
        if title: args += ["--title", title]
        args += ["--", "bash", "-c", f"{cmd}; echo 'Command completed, press Enter to close'; read"]
        p = subprocess.Popen(args)
    # Handle other platforms if needed
    processes.append(p)
    return p

def run_command(cmd):
    """Run command directly and return a process that can be waited on."""
    p = subprocess.Popen(cmd, shell=True)
    processes.append(p)
    return p

def shutdown(signum, frame):
    """Terminate all child processes."""
    print(f"↪ got signal {signum}, terminating children…")
    for p in processes:
        p.terminate()

# Register signal handler
signal.signal(signal.SIGUSR1, shutdown)

if __name__ == "__main__":
    # TODO: change to the list of objects
    list_of_objects = ["orange", "apple", "sports ball", "cup"]  
    
    # TODO: change to the image path
    llama = LlamaPrompt(image_path="/home/cs225a1/ina/8VC-Hackathon/d405_image_10.png")  
    result = llama.prompt_llama(list_of_objects)
    print(result)
    
    # Process each object
    for object_name, bag_name in result:
        # Start the appropriate visual servoing demo based on bag classification
        if bag_name == "food":
            p1 = run_command("python3 visual_servoing_demo.py -A")
        elif bag_name == "non-food":
            p1 = run_command("python3 visual_servoing_demo.py -B")
            
        # Start the perception script for the specific object
        p2 = run_command(f"python3 yolo_servo_perception.py -c {object_name}")
        
        # Wait for both processes to complete before moving to the next object
        print(f"Processing object: {object_name}...")
        p1.wait()
        p2.wait()
        print(f"Completed processing: {object_name}")

    try:
        # Keep the main process alive until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown(None, None)