#!/usr/bin/env python3

import subprocess
import threading

def start_reading(quantity=1):
    subprocess.check_output(["python3", "./main.py", "--mode", "read"])

def start_writting(quantity=1):
    subprocess.check_output(["python3", "./main.py", "--mode", "write"])

r = threading.Thread(target=start_reading, args=(1,))
r.start()

w = threading.Thread(target=start_writting, args=(1,))
w.start()
