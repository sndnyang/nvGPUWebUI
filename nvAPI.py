#!/usr/bin/env python

import re
import subprocess
from os import environ, getcwd

MEMORY_FREE_RATIO = 0.05
MEMORY_MODERATE_RATIO = 0.9
GPU_FREE_RATIO = 0.05
GPU_MODERATE_RATIO = 0.75

# parse the command length argument
command_length = 100


def get_process_info():
    fake_stdin_path = "nvidia-smi-output.txt"
    processes = subprocess.run(["nvidia-smi", "-f", fake_stdin_path])
    with open(fake_stdin_path, 'rt') as f:
        lines = f.readlines()

    i = 0
    for i in range(len(lines)):
        if lines[i].startswith("| Processes:"):
            i += 3
            break

    # Parse the PIDs from the lower part
    gpu_num = []
    pid = []
    gpu_mem = []
    user = []
    cpu = []
    mem = []
    time = []
    command = []

    while not lines[i].startswith("+--"):
        if "Not Supported" in lines[i]:
            i += 1
            continue
        line = lines[i]
        line = re.split(r'\s+', line)
        gpu_num.append(line[1])
        pid.append(line[2])
        gpu_mem.append(line[-3])
        user.append("")
        cpu.append("")
        mem.append("")
        time.append("")
        command.append("")
        i += 1

    # Query the PIDs using ps
    ps_format = "pid,user,%cpu,%mem,etime,command"
    processes = subprocess.run(["ps", "-o", ps_format, "-p", ",".join(pid)], stdout=subprocess.PIPE)

    # Parse ps output
    for line in processes.stdout.decode().split("\n"):
        if line.strip().startswith("PID") or len(line) == 0:
            continue
        parts = re.split(r'\s+', line.strip(), 5)
        idx = pid.index(parts[0])
        user[idx] = parts[1]
        cpu[idx] = parts[2]
        mem[idx] = parts[3]
        time[idx] = parts[4] if not "-" in parts[4] else parts[4].split("-")[0] + " days"
        command[idx] = parts[5][0:100]

    process_list = []
    user_me = (lambda: environ["USERNAME"] if "C:" in getcwd() else environ["USER"])()
    for i in range(len(pid)):
        process_list.append((
            gpu_num[i],
            pid[i],
            user[i],
            gpu_mem[i],
            cpu[i],
            mem[i],
            time[i],
            command[i],
            user[i] == user_me
        ))
    return process_list
