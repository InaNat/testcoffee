import subprocess
import platform
import time
from send_req_llama import LlamaPrompt

def run_in_new_terminal(cmd, title=None):
    """Run a command in its own terminal window."""
    system = platform.system()
    if system == "Linux":
        args = ["gnome-terminal"]
        if title:
            args += ["--title", title]
        # the `read` at the end keeps the terminal open so you can inspect output
        args += ["--", "bash", "-c", f"{cmd}; echo 'Done, press Enter to close'; read"]
        return subprocess.Popen(args)
    else:
        # fall back to simple background process
        return subprocess.Popen(cmd, shell=True)

def kill_process(proc):
    try:
        proc.terminate()
    except Exception:
        pass
    # optionally: proc.kill()

if __name__ == "__main__":
    # your list of object names
    list_of_objects = ["orange", "apple", "sports ball", "cup"]

    # fire off your image‐sending script once
    p_img = run_in_new_terminal("python3 send_d405_images.py", title="send_d405_images")

    # get your (object, bag) pairs from llama
    llama = LlamaPrompt(image_path="/home/cs225a1/ina/8VC-Hackathon/d405_image_10.png")
    result = llama.prompt_llama(list_of_objects)
    print("LLM result:", result)

    for object_name, bag_name in result:
        # build the two commands
        cmd1 = f"python3 yolo_servo_perception.py -c {object_name}"
        cmd2 = "python3 visual_servoing_demo.py -A" if bag_name == "food" else "python3 visual_servoing_demo.py -B"

        # launch each in its own terminal
        p1 = run_in_new_terminal(cmd1, title=f"{object_name}-yolo")
        p2 = run_in_new_terminal(cmd2, title=f"{object_name}-servo")

        print(f"→ Launched p1={p1.pid}, p2={p2.pid} for '{object_name}'")

        # **only** wait for p2
        p2.wait()
        print(f"← p2 ({p2.pid}) exited; killing p1 ({p1.pid})…")

        # now kill p1
        kill_process(p1)
        p1.wait()
        print(f"✔ Finished processing '{object_name}'\n")

    # when you're all done you can optionally kill p_img too
    kill_process(p_img)
    print("All done.")
