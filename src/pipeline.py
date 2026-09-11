import subprocess
import sys


def run_step(script_name):
    print("\n" + "=" * 60)
    print(f"Running: {script_name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, f"src/{script_name}"],
        check=False
    )

    if result.returncode != 0:
        print(f"\nERROR: {script_name} failed.")
        sys.exit(result.returncode)

    print(f"\nCompleted: {script_name}")


def main():
    print("\n" + "=" * 60)
    print("EV CHARGE INTELLIGENCE - FULL DATA PIPELINE")
    print("=" * 60)

    run_step("clean.py")
    run_step("transform.py")
    run_step("analyze.py")
    run_step("visualize.py")

    print("\n" + "=" * 60)
    print("FULL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()