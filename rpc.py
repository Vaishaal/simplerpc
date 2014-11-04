import os
import subprocess
def factorial(n):
    if n == 1:
        return 1
    return n*factorial(n-1)

def ls(d="."):
    return subprocess.check_output("ls {0}".format(d), shell=True)
