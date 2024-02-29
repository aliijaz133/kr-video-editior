import os
import subprocess


def run_main():
    subprocess.Popen(
        ["python", "main.py"], cwd=os.path.dirname(os.path.abspath(__file__))
    )


if __name__ == "__main__":
    run_main()
