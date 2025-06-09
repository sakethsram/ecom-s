import os
import subprocess

# Define the commands to run each script in a new terminal
commands = [
    'gnome-terminal -- bash -c "python3 amazon_main.py; exec bash"',
    'gnome-terminal -- bash -c "python3 flipkart_main.py; exec bash"',
    'gnome-terminal -- bash -c "python3 sapna_main.py; exec bash"',
]

for cmd in commands:
    subprocess.Popen(cmd, shell=True)

print("Launched amazon_main.py, flipkart_main.py, and sapna_main.py in new terminals.")