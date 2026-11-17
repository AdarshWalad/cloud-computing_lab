import subprocess
import time
import os

WORKLOADS = [
    ("W1", 1),
    ("W2", 2),
    ("W3", 4),
    ("W4", 8),
    ("W5", 16)
]

def run_workloads():
    print("Starting automated workloads for Music App...")
    
    for name, users in WORKLOADS:
        print(f"\n=== {name}: {users} concurrent user(s), 60 s ===")
        
        # Run locust headless
        cmd = [
            "python", "-m", "locust",
            "-f", "loadtest/locustfile.py",
            "--headless",
            "-u", str(users),
            "-r", str(users),
            "-t", "60s",
            "--host", "http://127.0.0.1:8003"
        ]
        
        # Run the command and print output to terminal just like the screenshots
        subprocess.run(cmd)
        
        if name != "W5":
            print(f"\nFinished {name}. Waiting 10 seconds before the next workload cools down...")
            time.sleep(10)

if __name__ == "__main__":
    run_workloads()
